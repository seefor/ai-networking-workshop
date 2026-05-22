# Episode 1 Workshop Outline

## Title

Build Your First AI Network Automation Tool with Python, Claude, P.E.N.E., and MCP

## Target Duration

3 hours

## Big Idea

Most network automation starts with a script. That script logs into a device, runs a command, and gives you output.

Useful? Yes.

Intelligent? Not yet.

In this workshop, we take that normal Python network automation script and evolve it into an AI-callable MCP tool.

## Learning Objectives

By the end, learners should be able to:

1. Explain why LLMs need tools for network operations.
2. Use Python dictionaries, functions, and YAML inventory for network automation.
3. Connect to Arista cEOS devices in Containerlab.
4. Send structured network data to Claude.
5. Use P.E.N.E. to make network prompts safer and more consistent.
6. Run a basic MCP server that exposes read-only network tools.

## Timing

### 0:00-0:20 - Why AI Needs Network Tools

Explain the problem with asking an LLM to troubleshoot a network without access to real state.

Key line:

> A chatbot can guess. A tool-using assistant can check.

### 0:20-0:55 - Python for Network Engineers

Use `scripts/01_python_basics.py` and `scripts/02_inventory_loader.py`.

Teach only what is needed:

- strings
- dictionaries
- lists
- functions
- YAML inventory
- environment variables

### 0:55-1:30 - Talk to the Arista Lab

Deploy the lab:

```bash
make lab-up
```

Run:

```bash
python scripts/03_connect_to_device.py leaf1
python scripts/04_get_interfaces.py leaf1
```

### 1:30-2:00 - Calling Claude

Show the difference between:

```text
Parse this config.
```

And a structured P.E.N.E. prompt.

Run:

```bash
python scripts/05_claude_pene_analysis.py examples/interface_output.json
```

### 2:00-2:25 - P.E.N.E. for Network AI

Cover:

- Persona & Purpose
- Examples
- kNowledge & coNstraints
- Evaluation

Use `prompts/pene_network_analysis_prompt.txt`.

### 2:25-2:55 - Build Your First MCP Server

Run:

```bash
python mcp_server/server.py
```

Connect MCP Inspector to:

```text
http://localhost:8000/mcp
```

Demo tools:

- `list_devices`
- `get_device_facts`
- `check_interfaces`
- `run_safe_show_command`

### 2:55-3:00 - Wrap-Up

Close with:

> Today we moved from a Python script to an AI-callable network tool. In the next episode, we will turn this into a troubleshooting assistant.
