# MCP Client Config Examples

## MCP Inspector

Start the server:

```bash
python mcp_server/server.py
```

Start MCP Inspector:

```bash
npx -y @modelcontextprotocol/inspector
```

Connect to:

```text
http://localhost:8000/mcp
```

## Claude Code Example

After starting the server, add it to Claude Code with HTTP transport:

```bash
claude mcp add --transport http ai-network-automation http://localhost:8000/mcp
```

Then ask Claude Code:

```text
Use the AI Network Automation MCP tools to list the lab devices.
```

## Example Questions

```text
What devices are in the lab?
```

```text
Check interfaces on leaf1.
```

```text
Run show ip bgp summary on spine1.
```

```text
Based on the interface status, what should I check next?
```
