"""Generate deterministic interface configuration snippets."""

from __future__ import annotations


def generate_interface_commands(
    prefix: str,
    suffix: str,
    *,
    start: int = 0,
    stop: int = 47,
) -> list[str]:
    """Build inclusive interface commands from ``start`` through ``stop``."""
    if start < 0 or stop < 0:
        raise ValueError("interface indexes cannot be negative")
    if start > stop:
        raise ValueError("start must be less than or equal to stop")
    if not prefix.strip():
        raise ValueError("prefix cannot be empty")
    return [f"{prefix}{index}{suffix}".strip() for index in range(start, stop + 1)]
