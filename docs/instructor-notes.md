# Instructor Notes

## Teaching Positioning

Do not present this as four separate topics:

- Python
- Claude
- P.E.N.E.
- MCP

Present it as one journey:

> We are turning normal network automation scripts into AI-callable tools.

## Recommended Teaching Flow

Keep reminding learners of the stack:

```text
Network device
↓
Python function
↓
Structured network data
↓
Claude reasoning
↓
P.E.N.E. safety and consistency
↓
MCP tool exposure
```

## Important Safety Message

Episode 1 is read-only.

That is intentional.

Learners should build trust before they build change automation.

## Instructor Demo Tips

### Demo 1

Show a vague prompt first:

```text
Parse this config.
```

Then explain why that is dangerous:

- no role
- no output format
- no constraints
- no safety boundary
- no evaluation criteria

### Demo 2

Show the P.E.N.E. prompt.

Emphasize:

> Good prompts do not make the model magic. Good prompts reduce ambiguity.

### Demo 3

Run the MCP server and show how an AI client can discover tools.

Key phrase:

> MCP lets the assistant call the same network functions we already trust from Python.

## Common Troubleshooting

### cEOS image missing

If Containerlab fails because it cannot find the cEOS image, import it into Docker first:

```bash
docker import cEOS64-lab-4.32.0F.tar.xz ceos:4.32.0F
```

### Cannot SSH to device

Check that the lab is up:

```bash
docker ps
```

Check the generated container names:

```bash
containerlab inspect -t lab/topology.clab.yml
```

### Claude API error

Confirm `.env` exists and includes:

```bash
ANTHROPIC_API_KEY=your_key
```

### MCP Inspector cannot connect

Confirm the server is running:

```bash
python mcp_server/server.py
```

Then connect to:

```text
http://localhost:8000/mcp
```
