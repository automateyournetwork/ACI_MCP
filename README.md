# 🚀 ACI FastMCP Server

A Model Context Protocol (MCP) server that provides full **CRUD access** to the Cisco ACI API via structured natural language tools. This server exposes all relevant ACI endpoints from a configurable `urls.json` file and dynamically builds tools for read (GET) and write (POST) operations.

Built on the [FastMCP](https://github.com/modelcontext/fastmcp) framework and fully compatible with LangGraph, Claude, ChatGPT, and VS Code Copilot for AI-assisted infrastructure operations.

---

## 🔧 Features

- ✅ Token-based Cisco APIC authentication
- ✅ Full support for `GET` and `POST` (CRUD-ready with optional `PUT`, `DELETE`)
- ✅ Support for **grouped and ungrouped** ACI endpoints
- ✅ Validates and auto-wraps APIC-compliant payloads
- ✅ STDIO-compatible for use in Claude, VS Code, or LangGraph
- ✅ Uses `.env` and structured logging
- 🧠 Auto-discovers tool schema from JSON

---

## 📁 Folder Structure

```bash
ACI_MCP/
├── aci_mcp/
│   ├── main.py           # MCP server
│   └── urls.json         # Endpoints grouped by category
├── .env                  # Your secrets (APIC_URL, USERNAME, PASSWORD)
├── README.md             # This file
🧪 Environment Variables
Create a .env file in the root of your project:

env
Copy
Edit
APIC_URL=https://sandboxapicdc.cisco.com
USERNAME=admin
PASSWORD=!v3G@!4@Y
URLS_PATH=aci_mcp/urls.json
🚀 How to Run
🧑‍💻 In VS Code (Copilot / LangGraph):
Use the following JSON entry in your MCP client config:

json
Copy
Edit
"aci": {
  "type": "stdio",
  "command": "wsl",
  "args": [
    "env",
    "APIC_URL=https://sandboxapicdc.cisco.com",
    "USERNAME=admin",
    "PASSWORD=!v3G@!4@Y",
    "URLS_PATH=/home/johncapobianco/ACI_MCP/aci_mcp/urls.json",
    "python3",
    "/home/johncapobianco/ACI_MCP/aci_mcp/main.py"
  ]
}
This launches the MCP server inside WSL, using stdin/stdout for tool discovery and calling.

🤖 In Claude or any A2A-compatible agent:
Claude-compatible assistants can auto-discover tools using this STDIO-based server via Model Context Protocol.

📦 Tools Exposed
Grouped tools (e.g. BGP, L3, L2): one tool per group, with dynamic endpoint selection

Ungrouped tools: each endpoint gets its own:

GET tool (e.g. tenants_get)

POST tool (e.g. tenants_post)

🧠 Example Prompts
How many tenants are in my fabric?
Create a tenant named MCP_Tenant
Get all IP addresses
Show me BGP peers and Route Reflectors
Get the health status of the fabric
Post to /api/node/mo/uni/tn-NewTenant.json with status "created"

📄 Example POST Payload
json
Copy
Edit
{
  "fvTenant": {
    "attributes": {
      "name": "MCP_Tenant",
      "rn": "tn-MCP_Tenant",
      "status": "created"
    }
  }
}
Make sure you include "status": "created" and correct rn (e.g., tn-<name>) for APIC to accept the POST.

📘 Extending It
You can easily extend this server:

Add more groups to urls.json

[
  {
    "Group": "L3",
    "Endpoints": [
      {
        "URL": "/api/node/class/l3extOut.json",
        "Name": "Layer 3 Out"
      },
      {
        "URL": "/api/node/class/l3extDomP.json",
        "Name": "L3 Domains"
      },
      {
        "URL": "/api/node/class/ipv4Addr.json",
        "Name": "IPv4 Addresses"
      },
      {
        "URL": "/api/node/class/ipv4Dom.json",
        "Name": "IPv4 Domains"
      },
      {
        "URL": "/api/node/class/ipv4Entity.json",
        "Name": "IPv4 Entities"
      },
      {
        "URL": "/api/node/class/ipv4If.json",
        "Name": "IPv4 Interfaces"
      },
      {
        "URL": "/api/node/class/ipv4Inst.json",
        "Name": "IPv4 Instances"
      },
      {
        "URL": "/api/node/class/ipv4Nexthop.json",
        "Name": "IPv4 Next Hop"
      },
      {
        "URL": "/api/node/class/ipv4Route.json",
        "Name": "IPv4 Routes"
      },
      {
        "URL": "/api/node/class/isisAdjEp.json",
        "Name": "ISIS Adjacency Endpoints"
      },
      {
        "URL": "/api/node/class/isisDTEp.json",
        "Name": "ISIS Discovered Tunnel Endpoints"
      },
      {
        "URL": "/api/node/class/isisDom.json",
        "Name": "ISIS Domains"
      },
      {
        "URL": "/api/node/class/isisDomLvl.json",
        "Name": "ISIS Domains Level"
      },
      {
        "URL": "/api/node/class/isisEntity.json",
        "Name": "ISIS Entities"
      },
      {
        "URL": "/api/node/class/isisIf.json",
        "Name": "ISIS Interfaces"
      },
      {
        "URL": "/api/node/class/isisIfLvl.json",
        "Name": "ISIS Interfaces Level"
      },
      {
        "URL": "/api/node/class/isisInst.json",
        "Name": "ISIS Instances"
      },
      {
        "URL": "/api/node/class/isisNexthop.json",
        "Name": "ISIS Next Hop"
      },
      {
        "URL": "/api/node/class/isisRoute.json",
        "Name": "ISIS Routes"
      },
      {
        "URL": "/api/node/class/l3Ctx.json",
        "Name": "L3 Contexts"
      },
      {
        "URL": "/api/node/class/l3EncRtdIf.json",
        "Name": "L3 Subinterfaces"
      },
      {
        "URL": "/api/node/class/l3Inst.json",
        "Name": "L3 Instances"
      },
      {
        "URL": "/api/node/class/l3LbRtdIf.json",
        "Name": "L3 Routed Loopback Interfaces"
      },
      {
        "URL": "/api/node/class/l3RsEncPhysRtdConf.json",
        "Name": "L3 Physical Interface Source Relationships"
      },
      {
        "URL": "/api/node/class/l3RtdIf.json",
        "Name": "L3 Routed Interfaces"
      },
      {
        "URL": "/api/node/class/l3extInstP.json",
        "Name": "L3Out Profiles"
      },
      {
        "URL": "/api/node/class/l3extIp.json",
        "Name": "L3Out IP Addresses"
      },
      {
        "URL": "/api/node/class/l3extLIfP.json",
        "Name": "L3 Logical Interface Profiles"
      },
      {
        "URL": "/api/node/class/l3extLNodeP.json",
        "Name": "L3 Logical Node Profiles"
      },
      {
        "URL": "/api/node/class/l3extMember.json",
        "Name": "L3Out Members"
      },
      {
        "URL": "/api/node/class/l3extRsEctx.json",
        "Name": "L3 Contexts Source Relationships"
      },
      {
        "URL": "/api/node/class/l3extRsL3DomAtt.json",
        "Name": "L3 Domains Source Relationships"
      },
      {
        "URL": "/api/node/class/l3extRsNodeL3OutAtt.json",
        "Name": "L3Out Node Source Relationships"
      },
      {
        "URL": "/api/node/class/l3extRsPathL3OutAtt.json",
        "Name": "L3Out Path Source Relationships"
      },
      {
        "URL": "/api/node/class/l3extSubnet.json",
        "Name": "L3 Subnets"
      },
      {
        "URL": "/api/node/class/acllogDropL3Flow.json",
        "Name": "L3Drops"
      },
      {
        "URL": "/api/node/class/acllogDropL3Pkt.json",
        "Name": "L3PktDrops"
      },
      {
        "URL": "/api/node/class/ospfAdjEp.json",
        "Name": "OSPF Adjacency Endpoints"
      },
      {
        "URL": "/api/node/class/ospfArea.json",
        "Name": "OSPF Areas"
      },
      {
        "URL": "/api/node/class/ospfDb.json",
        "Name": "OSPF Database"
      },
      {
        "URL": "/api/node/class/ospfDom.json",
        "Name": "OSPF Domains"
      },
      {
        "URL": "/api/node/class/ospfEntity.json",
        "Name": "OSPF Entities"
      },
      {
        "URL": "/api/node/class/ospfExtP.json",
        "Name": "OSPF External Profiles"
      },
      {
        "URL": "/api/node/class/ospfIf.json",
        "Name": "OSPF Interfaces"
      },
      {
        "URL": "/api/node/class/ospfInst.json",
        "Name": "OSPF Instances"
      },
      {
        "URL": "/api/node/class/ospfRoute.json",
        "Name": "OSPF Routes"
      },
      {
        "URL": "/api/node/class/ospfUcNexthop.json",
        "Name": "OSPF Unicast Next Hop"
      },
      {
        "URL": "/api/node/class/uribv4Db.json",
        "Name": "Unicast Route Database"
      },
      {
        "URL": "/api/node/class/uribv4Dom.json",
        "Name": "Unicast Route Domains"
      },
      {
        "URL": "/api/node/class/uribv4Entity.json",
        "Name": "Unicast Route Entities"
      },
      {
        "URL": "/api/node/class/uribv4Nexthop.json",
        "Name": "Unicast Route Next Hop"
      },
      {
        "URL": "/api/node/class/uribv4Route.json",
        "Name": "Unicast Routes"
      }
    ]
  },
  {
    "Group": "L2",
    "Endpoints": [
      {
        "URL": "/api/node/class/l2extOut.json",
        "Name": "Layer 2 Out"
      },
      {
        "URL": "/api/node/class/fvnsEncapBlk.json",
        "Name": "VLAN Encapsulation Blocks"
      },
      {
        "URL": "/api/node/class/fvnsVlanInstP.json",
        "Name": "VLAN Namespace Policies"
      },
      {
        "URL": "/api/node/class/infraRsVlanNs.json",
        "Name": "VLAN Namespace Source Relationships"
      },
      {
        "URL": "/api/node/class/l2BD.json",
        "Name": "L2 Bridge Domains"
      },
      {
        "URL": "/api/node/class/l2ExtIf.json",
        "Name": "L2 External Interfaces"
      },
      {
        "URL": "/api/node/class/l2RsEthIf.json",
        "Name": "L2 Interface Source Relationships"
      },
      {
        "URL": "/api/node/class/l2extInstP.json",
        "Name": "L2 External Instance Profiles"
      },
      {
        "URL": "/api/node/class/l2extLIfP.json",
        "Name": "L2 External Logical Interface Profiles"
      },
      {
        "URL": "/api/node/class/l2extLNodeP.json",
        "Name": "L2 External Logical Node Profiles"
      },
      {
        "URL": "/api/node/class/l2extRsEBd.json",
        "Name": "L2 EPG Bridge Domain Source Relationships"
      },
      {
        "URL": "/api/node/class/l2extRsPathL2OutAtt.json",
        "Name": "L2Out Paths"
      },
      {
        "URL": "/api/node/class/vlanCktEp.json",
        "Name": "VLAN Endpoint Group Encapsulation"
      }
    ]
  },
  {
    "Group": "Fabric",
    "Endpoints": [
      {
        "URL": "/api/node/class/fabricNode.json",
        "Name": "Fabric Nodes"
      },
      {
        "URL": "/api/node/class/fabricPod.json",
        "Name": "Fabric Pods"
      },
      {
        "URL": "/api/node/class/fabricPath.json",
        "Name": "Fabric Paths"
      },
      {
        "URL": "/api/node/class/fabricExtPathEpCont.json",
        "Name": "Fabric Extended Path Endpoint Containers"
      },
      {
        "URL": "/api/node/class/fabricInst.json",
        "Name": "Fabric Instances"
      },
      {
        "URL": "/api/node/class/fabricLink.json",
        "Name": "Fabric Links"
      },
      {
        "URL": "/api/node/class/fabricLinkCont.json",
        "Name": "Fabric Link Containers"
      },
      {
        "URL": "/api/node/class/fabricLooseLink.json",
        "Name": "Fabric Loose Links"
      },
      {
        "URL": "/api/node/class/fabricLooseNode.json",
        "Name": "Fabric Loose Nodes"
      },
      {
        "URL": "/api/node/class/fabricPathEp.json",
        "Name": "Fabric Path Endpoints"
      },
      {
        "URL": "/api/node/class/fabricPathEpCont.json",
        "Name": "Fabric Path Endpoint Containers"
      },
      {
        "URL": "/api/node/class/fabricProtPathEpCont.json",
        "Name": "Fabric Protected Path Endpoint Containers"
      }
    ]
  },
  {
    "Group": "Access Policies",
    "Endpoints": [
      {
        "URL": "/api/node/class/infraSpineP.json",
        "Name": "Spine Switch Profiles"
      },
      {
        "URL": "/api/node/class/infraAccBndlGrp.json",
        "Name": "Access Bundle Groups"
      },
      {
        "URL": "/api/node/class/infraCont.json",
        "Name": "Controllers"
      },
      {
        "URL": "/api/node/class/infraFexP.json",
        "Name": "FEX Policies"
      },
      {
        "URL": "/api/node/class/infraRsAccBaseGrp.json",
        "Name": "Access Policy Group Source Relationships"
      },
      {
        "URL": "/api/node/class/infraRsDomP.json",
        "Name": "Domain Profile Source Relationships"
      }
    ]
  },
  {
    "Group": "Contracts",
    "Endpoints": [
      {
        "URL": "/api/node/class/vzBrCP.json",
        "Name": "Contracts"
      },
      {
        "URL": "/api/node/class/vzEntry.json",
        "Name": "vzEntries"
      },
      {
        "URL": "/api/node/class/vzSubj.json",
        "Name": "Contract Subjects"
      },
      {
        "URL": "/api/node/class/vzAny.json",
        "Name": "vzAny"
      },
      {
        "URL": "/api/node/class/vzFilter.json",
        "Name": "vzFilters"
      },
      {
        "URL": "/api/node/class/vzRsAnyToCons.json",
        "Name": "vzAny To Consumers"
      },
      {
        "URL": "/api/node/class/vzRsAnyToProv.json",
        "Name": "vzAny To Providers"
      },
      {
        "URL": "/api/node/class/vzRsDenyRule.json",
        "Name": "vzDeny Rules"
      },
      {
        "URL": "/api/node/class/vzRsSubjFiltAtt.json",
        "Name": "Contract Subjects Filter Attributes"
      },
      {
        "URL": "/api/node/class/vzRtCons.json",
        "Name": "Contract Consumers Root"
      },
      {
        "URL": "/api/node/class/vzRtProv.json",
        "Name": "Contract Providers Root"
      },
      {
        "URL": "/api/node/class/vzRuleOwner.json",
        "Name": "vzRule Owner"
      },
      {
        "URL": "/api/node/class/vzTaboo.json",
        "Name": "vzTaboo"
      }
    ]
  },
  {
    "Group": "BGP",
    "Endpoints": [
      {
        "URL": "/api/node/class/bgpRRNodePEp.json",
        "Name": "BGP Route Reflectors"
      },
      {
        "URL": "/api/node/class/bgpDom.json",
        "Name": "BGP Domains"
      },
      {
        "URL": "/api/node/class/bgpDomAf.json",
        "Name": "BGP Domain Address Families"
      },
      {
        "URL": "/api/node/class/bgpEntity.json",
        "Name": "BGP Entities"
      },
      {
        "URL": "/api/node/class/bgpInst.json",
        "Name": "BGP Instances"
      },
      {
        "URL": "/api/node/class/bgpInstPol.json",
        "Name": "BGP Instances Policy"
      },
      {
        "URL": "/api/node/class/bgpPeer.json",
        "Name": "BGP Peers"
      },
      {
        "URL": "/api/node/class/bgpPeerAfEntry.json",
        "Name": "BGP Peers AF Entries"
      },
      {
        "URL": "/api/node/class/bgpPeerEntry.json",
        "Name": "BGP Peers Entries"
      },
      {
        "URL": "/api/node/class/bgpRRP.json",
        "Name": "BGP Route Reflector Policies"
      }
    ]
  },
  {
    "Group": "Interfaces",
    "Endpoints": [
      {
        "URL": "/api/node/class/infraPortS.json",
        "Name": "Interface Policies"
      },
      {
        "URL": "/api/node/class/pkiFabricNodeSSLCertificate.json",
        "Name": "Fabric Node SSL Certificates"
      },
      {
        "URL": "/api/node/class/cnwAggrIf.json",
        "Name": "Cluster Aggregate Interfaces"
      },
      {
        "URL": "/api/node/class/cnwPhysIf.json",
        "Name": "Cluster Physical Interfaces"
      },
      {
        "URL": "/api/node/class/arpIf.json",
        "Name": "ARP Interfaces"
      },
      {
        "URL": "/api/node/class/cnwRsMbrIfs.json",
        "Name": ""
      },
      {
        "URL": "/api/node/class/eqptFabP.json",
        "Name": "Equipment Fabric Ports"
      },
      {
        "URL": "/api/node/class/eqptLeafP.json",
        "Name": "Equipment Leaf Ports"
      },
      {
        "URL": "/api/node/class/eqptLocLed.json",
        "Name": "Equipment Port Locator LEDs"
      },
      {
        "URL": "/api/node/class/eqptRsIoPPhysConf.json",
        "Name": "Equipment RS IO Port Physical Configs"
      },
      {
        "URL": "/api/node/class/ethpmPhysIf.json",
        "Name": "Ethernet Port Manager Physical Interfaces"
      },
      {
        "URL": "/api/node/class/fvRsConsIf.json",
        "Name": "Contract Consumer Interfaces"
      },
      {
        "URL": "/api/node/class/infraAccPortGrp.json",
        "Name": "Access Port Groups"
      },
      {
        "URL": "/api/node/class/infraAccPortP.json",
        "Name": "Access Port Profiles"
      },
      {
        "URL": "/api/node/class/infraHPortS.json",
        "Name": "Host Port Selectors"
      },
      {
        "URL": "/api/node/class/infraPortBlk.json",
        "Name": "Port Blocks"
      },
      {
        "URL": "/api/node/class/infraSHPortS.json",
        "Name": "Spine Host Port Selectors"
      },
      {
        "URL": "/api/node/class/infraSpAccPortP.json",
        "Name": "Spine Access Port Profiles"
      },
      {
        "URL": "/api/node/class/lacpIf.json",
        "Name": "LACP Interfaces"
      },
      {
        "URL": "/api/node/class/leqptRsLsNodeToIf.json",
        "Name": "External Unmanaged Nodes Interfaces"
      },
      {
        "URL": "/api/node/class/mgmtMgmtIf.json",
        "Name": "Management Interfaces"
      },
      {
        "URL": "/api/node/class/pcAggrIf.json",
        "Name": "Port Channel Aggregate Interfaces"
      },
      {
        "URL": "/api/node/class/pcRsMbrIfs.json",
        "Name": "Port Channel Member Interfaces"
      },
      {
        "URL": "/api/node/class/sviIf.json",
        "Name": "SVIs"
      },
      {
        "URL": "/api/node/class/tunnelIf.json",
        "Name": "Tunnel Interfaces"
      },
      {
        "URL": "/api/node/class/vpcIf.json",
        "Name": "VPC Interfaces"
      },
      {
        "URL": "/api/node/class/vzRsIf.json",
        "Name": "vzInterface Source Relationships"
      }
    ]
  },
  {
    "Group": "Access Control",
    "Endpoints": [
      {
        "URL": "/api/node/class/actrlEntity.json",
        "Name": "Access Control Entities"
      },
      {
        "URL": "/api/node/class/actrlInst.json",
        "Name": "Access Control Instances"
      },
      {
        "URL": "/api/node/class/actrlRule.json",
        "Name": "Access Control Rules"
      },
      {
        "URL": "/api/node/class/actrlScope.json",
        "Name": "Access Control Scopes"
      }
    ]
  },
  {
    "Group": "Compute",
    "Endpoints": [
      {
        "URL": "/api/node/class/compCtrlr.json",
        "Name": "Compute Controllers"
      },
      {
        "URL": "/api/node/class/compDom.json",
        "Name": "Compute Domains"
      },
      {
        "URL": "/api/node/class/compEpPD.json",
        "Name": "Compute Endpoint Policy Descriptions"
      },
      {
        "URL": "/api/node/class/compProv.json",
        "Name": "Compute Providers"
      },
      {
        "URL": "/api/node/class/compRsDomP.json",
        "Name": "Cluster RS Member Interfaces"
      },
      {
        "URL": "/api/node/class/firmwareCompRunning.json",
        "Name": "Firmware Compute Running"
      }
    ]
  },
  {
    "Group": "CDP",
    "Endpoints": [
      {
        "URL": "/api/node/class/cdpAdjEp.json",
        "Name": "CDP Adjacency Endpoints"
      },
      {
        "URL": "/api/node/class/cdpEntity.json",
        "Name": "CDP Entities"
      },
      {
        "URL": "/api/node/class/cdpIf.json",
        "Name": "CDP Interfaces"
      },
      {
        "URL": "/api/node/class/cdpInst.json",
        "Name": "CDP Instances"
      },
      {
        "URL": "/api/node/class/cdpIntfAddr.json",
        "Name": "CDP Interface Addresses"
      },
      {
        "URL": "/api/node/class/cdpMgmtAddr.json",
        "Name": "CDP Management Addresses"
      }
    ]
  },
  {
    "Group": "Equipment",
    "Endpoints": [
      {
        "URL": "/api/node/class/eqptBSlot.json",
        "Name": "Equipment Board Slots"
      },
      {
        "URL": "/api/node/class/eqptBoard.json",
        "Name": "Equipment Boards"
      },
      {
        "URL": "/api/node/class/eqptCPU.json",
        "Name": "Equipment CPUs"
      },
      {
        "URL": "/api/node/class/eqptCh.json",
        "Name": "Equipment Chassis"
      },
      {
        "URL": "/api/node/class/eqptDimm.json",
        "Name": "Equipment DIMMs"
      },
      {
        "URL": "/api/node/class/eqptExtCh.json",
        "Name": "Equipment Fabric Extenders"
      },
      {
        "URL": "/api/node/class/eqptFan.json",
        "Name": "Equipment Fans"
      },
      {
        "URL": "/api/node/class/eqptFpga.json",
        "Name": "Equipment Field Programmable Gate Arrays"
      },
      {
        "URL": "/api/node/class/eqptFt.json",
        "Name": "Equipment Fan Trays"
      },
      {
        "URL": "/api/node/class/eqptFtSlot.json",
        "Name": "Equipment Fan Tray Slots"
      },
      {
        "URL": "/api/node/class/eqptIndLed.json",
        "Name": "Equipment Indicator LEDs"
      },
      {
        "URL": "/api/node/class/eqptLC.json",
        "Name": "Equipment Line Cards"
      },
      {
        "URL": "/api/node/class/eqptLCSlot.json",
        "Name": "Equipment Line Card Slots"
      },
      {
        "URL": "/api/node/class/eqptPsu.json",
        "Name": "Equipment Power Supplies"
      },
      {
        "URL": "/api/node/class/eqptPsuSlot.json",
        "Name": "Equipment Power Supply Slots"
      },
      {
        "URL": "/api/node/class/eqptSensor.json",
        "Name": "Equipment Sensors"
      },
      {
        "URL": "/api/node/class/eqptSpCmnBlk.json",
        "Name": "Equipment SP Common Blocks"
      },
      {
        "URL": "/api/node/class/eqptSpromLc.json",
        "Name": "Equipment SPROM LCs"
      },
      {
        "URL": "/api/node/class/eqptSpromPsu.json",
        "Name": "Equipment SPROM Power Supply"
      },
      {
        "URL": "/api/node/class/eqptSpromPsuBlk.json",
        "Name": "Equipment SPROM Power Supply Blocks"
      },
      {
        "URL": "/api/node/class/eqptSpromSup.json",
        "Name": "Equipment SPROM Supervisors"
      },
      {
        "URL": "/api/node/class/eqptStorage.json",
        "Name": "Equipment Storage"
      },
      {
        "URL": "/api/node/class/eqptSupC.json",
        "Name": "Equipment Supervisors"
      },
      {
        "URL": "/api/node/class/eqptSupCSlot.json",
        "Name": "Equipment Supervisor Slots"
      },
      {
        "URL": "/api/node/class/leqptLooseNode.json",
        "Name": "External Unmanaged Nodes"
      }
    ]
  },
  {
    "Group": "LLDP",
    "Endpoints": [
      {
        "URL": "/api/node/class/lldpAdjEp.json",
        "Name": "LLDP Adjacency Endpoints"
      },
      {
        "URL": "/api/node/class/lldpEntity.json",
        "Name": "LLDP Entities"
      },
      {
        "URL": "/api/node/class/lldpIf.json",
        "Name": "LLDP Interfaces"
      },
      {
        "URL": "/api/node/class/lldpInst.json",
        "Name": "LLDP Instances"
      }
    ]
  },
  {
    "Group": "VPC",
    "Endpoints": [
      {
        "URL": "/api/node/class/vpcDom.json",
        "Name": "VPC Domains"
      },
      {
        "URL": "/api/node/class/vpcEntity.json",
        "Name": "VPC Entities"
      },
      {
        "URL": "/api/node/class/vpcInst.json",
        "Name": "VPC Instances"
      },
      {
        "URL": "/api/node/class/vpcRsVpcConf.json",
        "Name": "VPC Configurations"
      }
    ]
  },
  {
    "URL": "/api/node/class/fvTenant.json",
    "Name": "Tenants"
  },
  {
    "URL": "/api/node/mo/uni.json",
    "Name": "Create Tenant at Root"
  },
  {
    "URL": "/api/node/class/fvAEPg.json",
    "Name": "Endpoint Groups"
  },
  {
    "URL": "/api/node/class/fvBD.json",
    "Name": "Bridge Domains"
  },
  {
    "URL": "/api/node/class/fvCtx.json",
    "Name": "Contexts"
  },
  {
    "URL": "/api/node/class/fvAp.json",
    "Name": "Application Profiles"
  },
  {
    "URL": "/api/node/class/topSystem.json",
    "Name": ""
  },
  {
    "URL": "/api/node/class/fvSubnet.json",
    "Name": ""
  },
  {
    "URL": "/api/node/class/fvCEp.json",
    "Name": "Subnets"
  },
  {
    "URL": "/api/node/class/infraNodeP.json",
    "Name": "Leaf Switch Profiles"
  },
  {
    "URL": "/api/node/class/infraAttEntityP.json",
    "Name": "Attachable Access Entity Profiles"
  },
  {
    "URL": "/api/node/class/physDomP.json",
    "Name": "Physical Domains"
  },
  {
    "URL": "/api/node/class/qosClass.json",
    "Name": "QOS Classes"
  },
  {
    "URL": "/api/node/class/faultSummary.json",
    "Name": "Fault Summary"
  },
  {
    "URL": "/api/node/class/fvIp.json",
    "Name": "IP Addresses"
  },
  {
    "URL": "/api/node/class/licenseEntitlement.json",
    "Name": "License Entitlements"
  },
  {
    "URL": "/api/node/class/infraProfile.json",
    "Name": "Interface Profiles"
  },
  {
    "URL": "/api/node/class/aaaUser.json",
    "Name": "Users"
  },
  {
    "URL": "/api/node/class/aaaDomain.json",
    "Name": "Security Domains"
  },
  {
    "URL": "/api/node/mo/topology/health.json",
    "Name": "Health"
  },
  {
    "URL": "/api/node/class/topSystem.json?query-target=subtree&target-subtree-class=firmwareCtrlrRunning",
    "Name": "Controller Firmware Running"
  },
  {
    "URL": "/api/node/mo/topology/pod-1/node-1/av.json?query-target=children&target-subtree-class=infraWiNode",
    "Name": "Wired Nodes (InfraWiredNodes)"
  },
  {
    "URL": "/api/node/class/vnsMDev.json",
    "Name": "Device Packages"
  },
  {
    "URL": "/api/node/class/arpAdjEp.json",
    "Name": "ARP Adjacency Endpoints"
  },
  {
    "URL": "/api/node/class/arpDb.json",
    "Name": "ARP Database"
  },
  {
    "URL": "/api/node/class/arpDom.json",
    "Name": "ARP Domain"
  },
  {
    "URL": "/api/node/class/arpEntity.json",
    "Name": "ARP Entity"
  },
  {
    "URL": "/api/node/class/arpInst.json",
    "Name": "ARP Instances"
  },
  {
    "URL": "/api/node/class/fcEntity.json",
    "Name": "Fibre Channel Entities"
  },
  {
    "URL": "/api/node/class/firmwareCardRunning.json",
    "Name": "Firmware Card Running"
  },
  {
    "URL": "/api/node/class/firmwareRunning.json",
    "Name": "Firmware Running"
  },
  {
    "URL": "/api/node/class/fvEpPCont.json",
    "Name": "Endpoint Profile Containers"
  },
  {
    "URL": "/api/node/class/fvLocale.json",
    "Name": "Locales"
  },
  {
    "URL": "/api/node/class/fvRsBDToOut.json",
    "Name": "Bridge Domains To Outside"
  },
  {
    "URL": "/api/node/class/fvRsBd.json",
    "Name": "EPG Bridge Domain Links"
  },
  {
    "URL": "/api/node/class/fvRsCons.json",
    "Name": "Contract Consumers"
  },
  {
    "URL": "/api/node/class/fvRsCtx.json",
    "Name": "Context Source Relationships"
  },
  {
    "URL": "/api/node/class/fvRsDomAtt.json",
    "Name": "Domain Attachments"
  },
  {
    "URL": "/api/node/class/fvRsPathAtt.json",
    "Name": "Path Attachments"
  },
  {
    "URL": "/api/node/class/fvRsProv.json",
    "Name": "Contract Providers"
  },
  {
    "URL": "/api/node/class/fvRtBd.json",
    "Name": "Bridge Domains Target Relationships"
  },
  {
    "URL": "/api/node/class/fvRtCtx.json",
    "Name": "Contexts Target Relationships"
  },
  {
    "URL": "/api/node/class/infraFuncP.json",
    "Name": "Function Policies"
  },
  {
    "URL": "/api/node/class/infraRsAttEntP.json",
    "Name": "Attachable Access Entity Profiles Source Relationships"
  },
  {
    "URL": "/api/node/class/infraRsSpAccGrp.json",
    "Name": "Spine Access Policy Groups"
  },
  {
    "URL": "/api/node/class/infraWiNode.json",
    "Name": "Wired Nodes (Topology)"
  },
  {
    "URL": "/api/node/class/ipNexthopP.json",
    "Name": "Static Route Next Hop Policies"
  },
  {
    "URL": "/api/node/class/ipRouteP.json",
    "Name": "Route Policies"
  },
  {
    "URL": "/api/node/class/lacpEntity.json",
    "Name": "LACP Entities"
  },
  {
    "URL": "/api/node/class/lacpInst.json",
    "Name": "LACP Instances"
  },
  {
    "URL": "/api/node/class/vmmCtrlrP.json",
    "Name": "VMM Controller Profiles"
  },
  {
    "URL": "/api/node/class/vmmDomP.json",
    "Name": "VMM Domain Profiles"
  },
  {
    "URL": "/api/node/class/vmmProvP.json",
    "Name": "VMM Provider Profiles"
  },
  {
    "URL": "/api/node/class/vmmUsrAccP.json",
    "Name": "VMM User Profiles"
  }
]