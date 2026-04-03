# Lab 4: Agentic Network Bot

Build an autonomous AI agent that operates network devices.

## Overview

This lab combines everything you've learned:
- LLM fundamentals
- Prompt engineering  
- Tool calling
- Conversation memory
- Agentic reasoning

## What You'll Build

A complete AI agent that can:
- Autonomously investigate network issues
- Query multiple devices
- Make multi-step decisions
- Troubleshoot intelligently

## Mock Network Topology

```
spine1 (192.168.0.11) ─┬─ leaf1 (192.168.0.21)
                       └─ leaf2 (192.168.0.22)
spine2 (192.168.0.12) ─┘
```

## Available Tools

1. `get_device_status()` - Device info
2. `get_bgp_summary()` - BGP neighbors
3. `get_interface_status()` - Interface state
4. `ping_device()` - Reachability
5. `execute_command()` - Show commands
6. `get_topology_info()` - Network structure

## Running the Lab

```bash
# Set API key
export ANTHROPIC_API_KEY=your-key

# Run the agent
python3 agentic_network_bot.py
```

## Example Queries

```python
bot = AgenticNetworkBot()

# Simple
bot.chat("What's the status of spine1?")

# Complex (multi-step)
bot.chat("Are all BGP sessions up?")

# Troubleshooting
bot.chat("Something is wrong - investigate")
```

## Key Concepts

- **Autonomous**: Agent decides which tools to call
- **Multi-step**: Can call multiple tools to solve problems
- **Production-ready**: Same code works with real devices

## Production Migration

Replace mock functions with real SSH:

```python
# Mock (workshop)
def get_device_status(device):
    return MOCK_DEVICES.get(device)

# Production
import paramiko
def get_device_status(device):
    ssh = paramiko.SSHClient()
    ssh.connect(device, ...)
    # Execute commands, parse output
    return parsed_data
```

Agent code stays the same!
