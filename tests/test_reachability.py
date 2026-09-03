import subprocess

import pytest

from network_tools import reachability
from network_tools.reachability import PingResult, ping, ping_command, ping_many


def test_ping_is_reachable_when_process_succeeds() -> None:
    calls = []

    def runner(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, "", "")

    result = ping("192.0.2.1", runner=runner)
    assert result.reachable is True
    assert calls[0][0][0] == "ping"
    assert calls[0][1]["check"] is False


def test_ping_rejects_empty_target() -> None:
    with pytest.raises(ValueError):
        ping("   ")


def test_ping_command_for_windows(monkeypatch) -> None:
    monkeypatch.setattr(reachability.platform, "system", lambda: "Windows")
    assert ping_command("example.com", count=3, timeout=4) == [
        "ping",
        "-n",
        "3",
        "-w",
        "4000",
        "example.com",
    ]


def test_ping_command_for_unix(monkeypatch) -> None:
    monkeypatch.setattr(reachability.platform, "system", lambda: "Linux")
    assert ping_command("example.com", count=1, timeout=2) == [
        "ping",
        "-c",
        "1",
        "-W",
        "2",
        "example.com",
    ]


@pytest.mark.parametrize("count,timeout", [(0, 1), (1, 0)])
def test_ping_command_rejects_invalid_options(count: int, timeout: int) -> None:
    with pytest.raises(ValueError):
        ping_command("example.com", count=count, timeout=timeout)


def test_ping_many_retains_order(monkeypatch) -> None:
    def fake_ping(target: str, **kwargs) -> PingResult:
        return PingResult(target, True, 0)

    monkeypatch.setattr(reachability, "ping", fake_ping)
    results = ping_many(["one.example", " ", "two.example"], workers=2)
    assert [result.target for result in results] == ["one.example", "two.example"]


def test_ping_many_rejects_invalid_worker_count() -> None:
    with pytest.raises(ValueError):
        ping_many(["example.com"], workers=0)
