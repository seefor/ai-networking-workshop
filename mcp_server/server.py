#!/usr/bin/env python3
"""MCP server for read-only network inspection tools."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from network_tools import (
    get_facts,
    get_interface_status,
    list_lab_devices,
    run_show_command,
)

load_dotenv()

mcp = FastMCP("AI Network Automation MCP", json_response=True)


@mcp.tool()
def list_devices() -> list[dict[str, str]]:
    """List the lab devices available for read-only network inspection."""
    return list_lab_devices()


@mcp.tool()
def get_device_facts(device_name: str) -> dict[str, str]:
    """Run 'show version' against a selected lab device and return the output."""
    return get_facts(device_name)


@mcp.tool()
def check_interfaces(device_name: str) -> dict[str, str]:
    """Run 'show interfaces status' against a selected lab device and return the output."""
    return get_interface_status(device_name)


@mcp.tool()
def run_safe_show_command(device_name: str, command: str) -> dict[str, str]:
    """
    Run a read-only show command against a selected lab device.

    Safety rule: command must start with 'show ' and must not contain blocked
    configuration or file-operation keywords.
    """
    return run_show_command(device_name, command)


@mcp.resource("inventory://devices")
def inventory_resource() -> str:
    """Explain how to discover lab devices."""
    return "Use the list_devices tool to see the available Arista cEOS lab devices."


if __name__ == "__main__":
    # FastMCP's streamable-http transport defaults to port 8000.
    # MCP_HOST and MCP_PORT are included for future extension/documentation.
    os.environ.setdefault("FASTMCP_HOST", os.getenv("MCP_HOST", "0.0.0.0"))
    os.environ.setdefault("FASTMCP_PORT", os.getenv("MCP_PORT", "8000"))
    mcp.run(transport="streamable-http")
