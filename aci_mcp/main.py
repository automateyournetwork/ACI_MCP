import os
import re
import json
import logging
import requests
import urllib3
import asyncio
from typing import Dict, Any, Optional, Literal, Union, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ACIMCPServer")

APIC_URL = os.getenv("APIC_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

if not APIC_URL or not USERNAME or not PASSWORD:
    logger.error("❌ Missing one or more required environment variables: APIC_URL, USERNAME, PASSWORD")

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

# ------------------------------- APIC Auth Controller -------------------------------

class ACIController:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password

    def get_token(self):
        login_url = f"{self.base_url}/api/aaaLogin.json"
        payload = {
            "aaaUser": {
                "attributes": {
                    "name": self.username,
                    "pwd": self.password
                }
            }
        }
        try:
            response = requests.post(login_url, json=payload, verify=False)
            response.raise_for_status()
            logger.info("✅ Authenticated with APIC.")
            return response.cookies
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Token auth failed: {e}")
            raise

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        url = f"{self.base_url}{endpoint}"
        return self._request("GET", url, params=params)

    def post(self, endpoint: str, payload: Dict[str, Any]):
        url = f"{self.base_url}{endpoint}"
        return self._request("POST", url, json=payload)

    def put(self, endpoint: str, payload: Dict[str, Any]):
        url = f"{self.base_url}{endpoint}"
        return self._request("PUT", url, json=payload)

    def delete(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        return self._request("DELETE", url)

    def _request(self, method: str, url: str, **kwargs):
        try:
            cookies = self.get_token()
            response = requests.request(
                method,
                url,
                headers=HEADERS,
                cookies=cookies,
                verify=False,
                timeout=15,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API error on {method} {url}: {e}")
            raise ToolError(f"{method} request failed: {e}")

aci_controller = ACIController(APIC_URL, USERNAME, PASSWORD)

class GroupToolInput(BaseModel):
    endpoint: str = Field(..., description="The endpoint URL within the group.")
    filter_expression: Optional[str] = Field(default=None)
    query_params: Optional[Dict[str, Any]] = Field(default=None)

# ------------------------------- Load URLs -------------------------------

def load_urls(file_path='urls.json') -> List[Dict[str, Any]]:
    try:
        with open(file_path, 'r') as f:
            raw = json.load(f)

        endpoints = []
        for item in raw:
            if "Group" in item:
                group = item["Group"]
                for ep in item["Endpoints"]:
                    ep["Group"] = group
                    endpoints.append(ep)
            else:
                item["Group"] = "ungrouped"
                endpoints.append(item)
        return endpoints
    except Exception as e:
        logger.error(f"❌ Failed to load URLS: {e}")
        return []

URLS = load_urls(os.getenv("URLS_PATH", "urls.json"))

# ------------------------------- FastMCP Setup -------------------------------

mcp = FastMCP(
    name="ACI MCP Server",
    instructions="Tools for full CRUD access to Cisco ACI API."
)
mcp.dependencies = []

# ------------------------------- Input Models -------------------------------

class FilterableToolInput(BaseModel):
    filter_expression: Optional[str] = Field(default=None)
    query_params: Optional[Dict[str, Any]] = Field(default=None)

class NonFilterableToolInput(BaseModel):
    query_params: Optional[Dict[str, Any]] = Field(default=None)

class CreateToolInput(BaseModel):
    payload: Dict[str, Any] = Field(..., description="JSON payload for POST.")

class UpdateToolInput(BaseModel):
    payload: Dict[str, Any] = Field(..., description="JSON payload for PUT.")

# ------------------------------- Tool Registration -------------------------------

# Group entries
grouped: Dict[str, List[Dict[str, Any]]] = {}

# Standalone entries
ungrouped: List[Dict[str, Any]] = []

# Separate into grouped and ungrouped
for entry in URLS:
    group = entry.get("Group", "ungrouped")
    if group == "ungrouped":
        ungrouped.append(entry)
    else:
        grouped.setdefault(group, []).append(entry)

# 1️⃣ Register grouped tools
for group, endpoints in grouped.items():
    endpoint_choices = [e["URL"] for e in endpoints if e.get("URL")]

    def make_group_tool(valid_endpoints, group_name):
        def group_tool(input: GroupToolInput) -> dict:
            if input.endpoint not in valid_endpoints:
                raise ToolError(f"Invalid endpoint for group '{group_name}'. Must be one of: {valid_endpoints}")
            args = {}
            if input.filter_expression:
                args["query-target-filter"] = input.filter_expression
            if input.query_params:
                args.update(input.query_params)
            return aci_controller.get(input.endpoint, args)
        return group_tool

    tool_base = re.sub(r'[^a-z0-9_-]', '_', group.replace(" ", "_").lower())
    tool_fn = make_group_tool(endpoint_choices, group)
    tool_fn.__name__ = f"{tool_base}_get"
    tool_fn.__doc__ = f"GET any endpoint from group '{group}' ({len(endpoint_choices)} endpoints)."
    mcp.add_tool(tool_fn)
    logger.info(f"✅ Registered grouped GET tool for {group} ({len(endpoint_choices)} endpoints)")

# 2️⃣ Register ungrouped tools as standalone CRUD
for entry in ungrouped:
    name = entry.get("Name", "") or entry["URL"].split("/")[-1]
    api_url_path = entry.get("URL")
    if not api_url_path:
        logger.warning(f"⚠️ Skipping: missing URL for {name}")
        continue

    tool_base = re.sub(r'[^a-z0-9_-]', '_', name.replace(" ", "_").lower())

    # READ
    def create_read_tool(endpoint: str):
        def tool(params: NonFilterableToolInput = Field(default_factory=NonFilterableToolInput)) -> dict:
            args = {}
            if params.query_params:
                args.update(params.query_params)
            return aci_controller.get(endpoint, args)
        return tool

    read_tool = create_read_tool(api_url_path)
    read_tool.__name__ = f"{tool_base}_get"
    read_tool.__doc__ = f"GET data for {name or api_url_path} from ACI (ungrouped)."
    mcp.add_tool(read_tool)

    # CREATE (POST)
    def create_post_tool(endpoint: str):
        def tool(input: CreateToolInput) -> dict:
            return aci_controller.post(endpoint, input.payload)
        return tool

    post_tool = create_post_tool(api_url_path)
    post_tool.__name__ = f"{tool_base}_post"
    post_tool.__doc__ = f"POST (create) data to {name or api_url_path} in ACI (ungrouped)."
    mcp.add_tool(post_tool)

    # DELETE
    def create_delete_tool(endpoint: str):
        def tool() -> dict:
            return aci_controller.delete(endpoint)
        return tool

    delete_tool = create_delete_tool(api_url_path)
    delete_tool.__name__ = f"{tool_base}_delete"
    delete_tool.__doc__ = f"DELETE resource at {name or api_url_path} in ACI (ungrouped)."
    mcp.add_tool(delete_tool)

    logger.info(f"✅ Registered individual GET tool for {name or api_url_path}")
# ------------------------------- Entry Point -------------------------------

async def _main_async():
    if not URLS:
        logger.error("❌ No tools registered.")
    else:
        try:
            tools_dict = await mcp.get_tools()
            logger.info(f"🚀 Starting ACI FastMCP with {len(tools_dict)} tools...")
        except Exception as e:
            logger.error(f"Tool discovery error: {e}")
        await mcp.run_async()

if __name__ == "__main__":
    asyncio.run(_main_async())
    logger.info("🚀 ACI FastMCP server is running.")