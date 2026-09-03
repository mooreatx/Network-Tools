from contextlib import contextmanager

import pytest

from network_tools.inventory import Device
from network_tools.netmiko_ops import (
    collect_facts,
    connection_parameters,
    restart_interfaces,
    update_dns_servers,
)


class FakeConnection:
    def __init__(self) -> None:
        self.commands = []
        self.saved = False

    def send_command(self, command):
        self.commands.append(command)
        return f"output: {command}"

    def send_config_set(self, commands):
        command_list = list(commands)
        self.commands.append(command_list)
        return "configured"

    def save_config(self):
        self.saved = True
        return "saved"


def fake_factory(connection):
    @contextmanager
    def factory(**kwargs):
        assert kwargs["password"] == "secret"
        yield connection

    return factory


def test_collect_facts() -> None:
    connection = FakeConnection()
    output = collect_facts(
        Device("lab", "192.0.2.1"),
        "user",
        "secret",
        factory=fake_factory(connection),
    )
    assert set(output) == {"version", "inventory", "interfaces"}


def test_update_dns_can_save() -> None:
    connection = FakeConnection()
    update_dns_servers(
        Device("lab", "192.0.2.1"),
        ["192.0.2.53"],
        "user",
        "secret",
        save=True,
        factory=fake_factory(connection),
    )
    assert connection.commands == [
        ["ip domain lookup", "no ip name-server", "ip name-server 192.0.2.53"]
    ]
    assert connection.saved is True


def test_restart_interfaces_uses_explicit_context() -> None:
    connection = FakeConnection()
    restart_interfaces(
        Device("lab", "192.0.2.1"),
        ["GigabitEthernet1/0/1"],
        "user",
        "secret",
        factory=fake_factory(connection),
    )
    assert connection.commands == [["interface GigabitEthernet1/0/1", "shutdown", "no shutdown"]]


def test_connection_parameters_rejects_missing_credentials() -> None:
    with pytest.raises(ValueError, match="required"):
        connection_parameters(Device("lab", "192.0.2.1"), "", "")


def test_update_dns_requires_server() -> None:
    with pytest.raises(ValueError, match="DNS"):
        update_dns_servers(Device("lab", "192.0.2.1"), [], "user", "secret")


def test_restart_interfaces_requires_interface() -> None:
    with pytest.raises(ValueError, match="interface"):
        restart_interfaces(Device("lab", "192.0.2.1"), [" "], "user", "secret")
