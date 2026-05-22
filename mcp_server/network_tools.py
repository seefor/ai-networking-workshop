"""Read-only network tools used by the MCP server."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from netmiko import ConnectHandler

INVENTORY_FILE = Path(__file__).resolve().parent / "inventory.yml"

BLOCKED_KEYWORDS = {
    "configure",
    "conf t",
    "reload",
    "copy",
    "delete",
    "erase",
    "write",
    "bash",
    "sudo",
    "enable secret",
    "username",
}

ALLOWED_PREFIXES = (
    "show ",
)


def load_inventory() -> dict[str, Any]:
    """Load devices from the YAML inventory."""
    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def list_lab_devices() -> list[dict[str, str]]:
    """Return a simple list of known lab devices."""
    inventory = load_inventory()
    results = []
    for name, device in inventory.get("devices", {}).items():
        results.append(
            {
                "name": name,
                "host": device["host"],
                "device_type": device["device_type"],
                "role": device.get("role", "unknown"),
            }
        )
    return results


def get_device(device_name: str) -> dict[str, Any]:
    """Return a device definition by inventory name."""
    inventory = load_inventory()
    devices = inventory.get("devices", {})
    if device_name not in devices:
        available = ", ".join(devices.keys())
        raise ValueError(f"Unknown device '{device_name}'. Available devices: {available}")
    return devices[device_name]


def is_safe_show_command(command: str) -> bool:
    """Allow only read-only show commands for the first workshop."""
    normalized = " ".join(command.strip().lower().split())
    if not normalized.startswith(ALLOWED_PREFIXES):
        return False
    return not any(blocked in normalized for blocked in BLOCKED_KEYWORDS)


def run_show_command(device_name: str, command: str) -> dict[str, str]:
    """Run a safe show command against a lab device."""
    if not is_safe_show_command(command):
        raise ValueError(
            "Blocked command. Episode 1 only allows read-only commands that start with 'show '."
        )

    device = get_device(device_name)
    connection_params = {
        "device_type": device["device_type"],
        "host": device["host"],
        "username": device["username"],
        "password": device["password"],
    }

    with ConnectHandler(**connection_params) as connection:
        output = connection.send_command(command)

    return {
        "device": device_name,
        "command": command,
        "output": output,
    }


def get_facts(device_name: str) -> dict[str, str]:
    """Collect basic facts from a lab device."""
    return run_show_command(device_name, "show version")


def get_interface_status(device_name: str) -> dict[str, str]:
    """Collect interface status from a lab device."""
    return run_show_command(device_name, "show interfaces status")
