# Lab 5: Reusable Network Tools with MCP

This lab extends the workshop from direct tool calling into reusable MCP-based tooling.

In the first four labs, the agent called Python functions directly. That is perfect for learning. But as soon as you want the same network tools to be reused by multiple AI clients, assistants, editors, or internal platforms, you need a cleaner packaging pattern.

That is where MCP, the Model Context Protocol, fits.

## What you will build

You will package the existing workshop network tools as an MCP server:

- `get_device_status`
- `get_interface_status`
- `get_bgp_summary`
- `ping_device`
- `execute_show_command`
- `get_topology_info`

The important idea is simple:

```text
Lab 4: Agent calls local Python functions directly
Lab 5: Agent/client discovers and calls those same tools through MCP
```

The business logic stays separate from the transport layer. That makes the tools easier to test, reuse, and eventually expose to other AI assistants.

## Why this matters for NetOps

Network teams already deal with tool sprawl: IPAM, monitoring, SSH, NMS, NetBox, controllers, CMDBs, and ticketing systems. Without a standard pattern, every AI assistant ends up needing custom glue for every system.

MCP gives you a consistent way to expose tools and context.

For this lab, we stay read-only and use the workshop mock network. That keeps the lesson safe while still showing the production pattern.

## Folder contents

```text
labs/lab5-mcp/
├── README.md          # This guide
├── mcp_server.py      # MCP server that exposes network tools
├── network_tools.py   # Safe wrapper around the workshop mock tools
└── client_test.py     # Local sanity test for the business logic
```

## Setup

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install mcp
```

The base workshop does not require MCP. This lab adds it as an optional dependency so the first four labs stay lightweight.

## Run the local tool test

Before testing MCP, confirm the underlying tool functions work:

```bash
python3 labs/lab5-mcp/client_test.py
```

You should see device status, BGP state, interface state, topology data, and a blocked unsafe command example.

## Run the MCP server

```bash
python3 labs/lab5-mcp/mcp_server.py
```

This starts a stdio-based MCP server. In a real client configuration, you would point your MCP-capable assistant or IDE at this command.

Example client configuration shape:

```json
{
  "mcpServers": {
    "ai-networking-workshop": {
      "command": "python3",
      "args": ["/absolute/path/to/ai-networking-workshop/labs/lab5-mcp/mcp_server.py"]
    }
  }
}
```

## Safety rules in this lab

This lab intentionally keeps the tools boring and safe:

- Only known workshop devices are allowed.
- Only `show` commands are allowed.
- Tool results are structured dictionaries.
- No configuration changes are exposed.
- Errors return data instead of crashing the agent.

That may sound restrictive, but this is exactly the pattern you want before connecting agents to real infrastructure.

## Suggested exercises

1. Add a new MCP tool for LLDP neighbor discovery.
2. Add a schema field that marks tool output as `mock` or `production`.
3. Add an allowlist for approved show commands.
4. Connect this server to an MCP-capable client and test the tool descriptions.
5. Compare direct Lab 4 tool calling against MCP tool discovery.

## Book alignment

This lab supports Chapter 8 of the book outline: **From lab agents to reusable tools with MCP**.

By the end of this lab, readers should understand when MCP is helpful, when direct tool calling is enough, and why the tool contract matters more than the agent hype.
