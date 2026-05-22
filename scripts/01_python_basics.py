#!/usr/bin/env python3
"""
Episode 1 - Part 1
Python basics for network engineers.

This is not a generic Python lesson. It is a quick walkthrough of the Python
building blocks we need before we talk to network devices and expose those
functions through MCP.
"""

from rich import print


def main() -> None:
    device_name = "leaf1"
    command = "show version"

    device = {
        "name": "leaf1",
        "host": "clab-ai-net-leaf1",
        "platform": "arista_eos",
        "username": "admin",
        "password": "admin",
    }

    devices = [
        device,
        {
            "name": "leaf2",
            "host": "clab-ai-net-leaf2",
            "platform": "arista_eos",
            "username": "admin",
            "password": "admin",
        },
    ]

    print("[bold]Python values we care about in network automation[/bold]")
    print(f"Device name: {device_name}")
    print(f"Command: {command}")
    print(f"One device dictionary: {device}")
    print(f"Device list: {devices}")

    print("\n[bold]Looping through devices[/bold]")
    for item in devices:
        print(f"Would connect to {item['name']} at {item['host']}")

    print("\n[bold]Function example[/bold]")
    print(build_show_command("interfaces status"))


def build_show_command(topic: str) -> str:
    """Build a simple show command from a topic."""
    return f"show {topic}"


if __name__ == "__main__":
    main()
