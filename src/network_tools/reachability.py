"""Cross-platform reachability checks with injectable process execution."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import platform
import subprocess


Runner = Callable[..., subprocess.CompletedProcess[str]]


@dataclass(frozen=True, slots=True)
class PingResult:
    target: str
    reachable: bool
    return_code: int


def ping_command(target: str, *, count: int = 2, timeout: int = 2) -> list[str]:
    """Create a ping command for the current operating system."""
    if count < 1 or timeout < 1:
        raise ValueError("count and timeout must be positive integers")
    if platform.system() == "Windows":
        return ["ping", "-n", str(count), "-w", str(timeout * 1000), target]
    return ["ping", "-c", str(count), "-W", str(timeout), target]


def ping(
    target: str,
    *,
    count: int = 2,
    timeout: int = 2,
    runner: Runner = subprocess.run,
) -> PingResult:
    """Check one target without invoking a shell."""
    if not target.strip():
        raise ValueError("target cannot be empty")
    completed = runner(
        ping_command(target, count=count, timeout=timeout),
        capture_output=True,
        check=False,
        text=True,
    )
    return PingResult(
        target=target,
        reachable=completed.returncode == 0,
        return_code=completed.returncode,
    )


def ping_many(
    targets: Iterable[str],
    *,
    count: int = 2,
    timeout: int = 2,
    workers: int = 10,
) -> list[PingResult]:
    """Check several targets concurrently while retaining input order."""
    target_list = [target.strip() for target in targets if target.strip()]
    if workers < 1:
        raise ValueError("workers must be a positive integer")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(
            executor.map(
                lambda target: ping(target, count=count, timeout=timeout),
                target_list,
            )
        )
