import json

from network_tools import cli
from network_tools.cli import main
from network_tools.reachability import PingResult


def test_mac_cli(capsys) -> None:
    assert main(["mac", "0011.2233.4455", "--format", "cisco"]) == 0
    assert capsys.readouterr().out.strip() == "0011.2233.4455"


def test_mac_cli_json(capsys) -> None:
    assert main(["mac", "001122334455"]) == 0
    assert json.loads(capsys.readouterr().out)["colon"] == "00:11:22:33:44:55"


def test_interfaces_cli(capsys) -> None:
    assert main(["interfaces", "interface ", " shutdown", "--start", "1", "--stop", "2"]) == 0
    assert capsys.readouterr().out.splitlines() == [
        "interface 1 shutdown",
        "interface 2 shutdown",
    ]


def test_ping_cli_reports_failure(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        cli,
        "ping_many",
        lambda *args, **kwargs: [PingResult("unreachable.example", False, 1)],
    )
    assert main(["ping", "unreachable.example"]) == 1
    assert json.loads(capsys.readouterr().out)[0]["reachable"] is False
