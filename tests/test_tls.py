"""Exercise APIC authentication and REST TLS with real Requests on loopback."""

import importlib
import json
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

import dotenv
import pytest
import requests
import trustme
from fastmcp.exceptions import ToolError


LOGIN_PATH = "/api/aaaLogin.json"
READ_PATH = "/api/node/class/fvTenant.json"
READ_RESULT = {"imdata": [], "totalCount": "0"}


@pytest.fixture
def controller_class(monkeypatch, tmp_path):
    # Import the real server without reading local credentials or registering tools.
    monkeypatch.setattr(dotenv, "load_dotenv", lambda: None)
    monkeypatch.setenv("APIC_URL", "https://127.0.0.1")
    monkeypatch.setenv("USERNAME", "test-user")
    monkeypatch.setenv("PASSWORD", "test-password")
    urls_path = tmp_path / "urls.json"
    urls_path.write_text("[]")
    monkeypatch.setenv("URLS_PATH", str(urls_path))
    monkeypatch.setenv("NO_PROXY", "*")
    monkeypatch.setenv("no_proxy", "*")
    netrc_path = tmp_path / "netrc"
    netrc_path.write_text("")
    monkeypatch.setenv("NETRC", str(netrc_path))
    monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
    monkeypatch.delenv("CURL_CA_BUNDLE", raising=False)
    return importlib.import_module("aci_mcp.main").ACIController


@pytest.fixture
def trusted_ca(controller_class, monkeypatch, tmp_path):
    ca = trustme.CA()
    ca_path = tmp_path / "ca.pem"
    ca.cert_pem.write_to_path(ca_path)
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", str(ca_path))
    return ca


@pytest.fixture
def https_server():
    servers = []

    def start(ca, hostname="127.0.0.1"):
        received = []

        class Handler(BaseHTTPRequestHandler):
            def respond(self):
                body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                received.append((self.command, self.path, body, self.headers))
                response = json.dumps(READ_RESULT).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                if self.path == LOGIN_PATH:
                    self.send_header("Set-Cookie", "APIC-cookie=test-token; Path=/; Secure")
                self.end_headers()
                self.wfile.write(response)

            do_GET = respond
            do_POST = respond

            def log_message(self, *args):
                pass

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ca.issue_cert(hostname).configure_cert(context)
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        server.socket = context.wrap_socket(server.socket, server_side=True)
        thread = Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
        thread.start()
        servers.append((server, thread))
        return f"https://127.0.0.1:{server.server_port}", received

    yield start

    for server, thread in reversed(servers):
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_login_and_rest_read_trust_configured_ca(controller_class, trusted_ca, https_server):
    url, received = https_server(trusted_ca)
    controller = controller_class(url, "test-user", "test-password")

    assert controller.get_token()["APIC-cookie"] == "test-token"
    assert controller.get(READ_PATH) == READ_RESULT
    assert [(method, path) for method, path, _, _ in received] == [
        ("POST", LOGIN_PATH), ("POST", LOGIN_PATH), ("GET", READ_PATH)
    ]
    assert json.loads(received[0][2]) == {
        "aaaUser": {"attributes": {"name": "test-user", "pwd": "test-password"}}
    }
    assert received[-1][3]["Cookie"] == "APIC-cookie=test-token"


@pytest.mark.parametrize("failure", ["untrusted_ca", "hostname_mismatch"])
def test_login_rejects_invalid_certificate(
    controller_class, trusted_ca, https_server, failure
):
    ca = trustme.CA() if failure == "untrusted_ca" else trusted_ca
    hostname = "wrong.example.test" if failure == "hostname_mismatch" else "127.0.0.1"
    url, received = https_server(ca, hostname)
    controller = controller_class(url, "test-user", "test-password")

    with pytest.raises(requests.exceptions.SSLError, match="CERTIFICATE_VERIFY_FAILED"):
        controller.get_token()

    # Rejection happens during TLS, before credentials or any HTTP request arrive.
    assert received == []


@pytest.mark.parametrize("failure", ["untrusted_ca", "hostname_mismatch"])
def test_rest_read_rejects_invalid_certificate(
    controller_class, trusted_ca, https_server, failure
):
    login_url, login_received = https_server(trusted_ca)
    ca = trustme.CA() if failure == "untrusted_ca" else trusted_ca
    hostname = "wrong.example.test" if failure == "hostname_mismatch" else "127.0.0.1"
    read_url, read_received = https_server(ca, hostname)
    controller = controller_class(login_url, "test-user", "test-password")

    # Authenticate against a trusted endpoint so login cannot mask a REST TLS bug.
    # Both network calls use real Requests, without a mocked HTTP client or token.
    with pytest.raises(ToolError, match="CERTIFICATE_VERIFY_FAILED") as error:
        controller._request("GET", f"{read_url}{READ_PATH}")

    assert isinstance(error.value.__context__, requests.exceptions.SSLError)
    assert [(method, path) for method, path, _, _ in login_received] == [("POST", LOGIN_PATH)]
    assert read_received == []


def test_default_ca_bundle_rejects_private_ca(controller_class, https_server):
    url, received = https_server(trustme.CA())
    controller = controller_class(url, "test-user", "test-password")

    with pytest.raises(requests.exceptions.SSLError, match="CERTIFICATE_VERIFY_FAILED"):
        controller.get_token()

    assert received == []
