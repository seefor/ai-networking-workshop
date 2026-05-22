#!/usr/bin/env python3
"""Connect to an Arista cEOS device and run show version."""

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException
from rich import print

REPO_ROOT = Path(__file__).resolve().parents[1]
INVENTORY_FILE = REPO_ROOT / "mcp_server" / "inventory.yml"


def load_inventory() -> dict[str, Any]:
    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def get_device_params(device_name: str) -> dict[str, Any]:
    inventory = load_inventory()
    devices = inventory.get("devices", {})
    if device_name not in devices:
        available = ", ".join(devices.keys())
        raise ValueError(f"Unknown device '{device_name}'. Available devices: {available}")
    return devices[device_name]


def run_command(device_name: str, command: str) -> str:
    device = get_device_params(device_name)
    connection_params = {
        "device_type": device["device_type"],
        "host": device["host"],
        "username": device["username"],
        "password": device["password"],
    }

    with ConnectHandler(**connection_params) as connection:
        return connection.send_command(command)


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")

    parser = argparse.ArgumentParser(description="Run show version against a lab device.")
    parser.add_argument("device", help="Device name from inventory.yml, for example leaf1")
    args = parser.parse_args()

    try:
        output = run_command(args.device, "show version")
    except (NetmikoAuthenticationException, NetmikoTimeoutException, ValueError) as exc:
        print(f"[red]Error:[/red] {exc}")
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
