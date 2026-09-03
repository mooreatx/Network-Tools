"""Testable Netmiko operations for Cisco IOS devices."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from contextlib import AbstractContextManager
from typing import Any, Protocol

from network_tools.inventory import Device


class Connection(Protocol):
    def send_command(self, command: str) -> str: ...
    def send_config_set(self, commands: Iterable[str]) -> str: ...
    def save_config(self) -> str: ...


ConnectionFactory = Callable[..., AbstractContextManager[Connection]]


def default_connection_factory(**kwargs: Any) -> AbstractContextManager[Connection]:
    """Create a Netmiko connection while keeping the dependency optional."""
    try:
        from netmiko import ConnectHandler
    except ImportError as error:
        raise RuntimeError("Install the 'automation' extra to use device commands") from error
    return ConnectHandler(**kwargs)


def connection_parameters(device: Device, username: str, password: str) -> dict[str, str]:
    """Build connection arguments without storing credentials in inventory."""
    if not username or not password:
        raise ValueError("username and password are required")
    return {
        "device_type": device.platform,
        "host": device.host,
        "username": username,
        "password": password,
    }


def collect_facts(
    device: Device,
    username: str,
    password: str,
    *,
    factory: ConnectionFactory = default_connection_factory,
) -> dict[str, str]:
    """Collect common read-only operational data from a device."""
    commands = {
        "version": "show version",
        "inventory": "show inventory",
        "interfaces": "show interfaces status",
    }
    with factory(**connection_parameters(device, username, password)) as connection:
        return {name: connection.send_command(command) for name, command in commands.items()}


def update_dns_servers(
    device: Device,
    servers: Iterable[str],
    username: str,
    password: str,
    *,
    save: bool = False,
    factory: ConnectionFactory = default_connection_factory,
) -> str:
    """Replace IOS name servers and optionally save the configuration."""
    server_list = list(servers)
    if not server_list:
        raise ValueError("at least one DNS server is required")
    commands = ["ip domain lookup", "no ip name-server", f"ip name-server {' '.join(server_list)}"]
    with factory(**connection_parameters(device, username, password)) as connection:
        output = connection.send_config_set(commands)
        if save:
            connection.save_config()
        return output


def restart_interfaces(
    device: Device,
    interfaces: Iterable[str],
    username: str,
    password: str,
    *,
    factory: ConnectionFactory = default_connection_factory,
) -> list[str]:
    """Administratively cycle explicitly supplied interfaces."""
    interface_list = [name.strip() for name in interfaces if name.strip()]
    if not interface_list:
        raise ValueError("at least one interface is required")
    with factory(**connection_parameters(device, username, password)) as connection:
        return [
            connection.send_config_set([f"interface {name}", "shutdown", "no shutdown"])
            for name in interface_list
        ]
