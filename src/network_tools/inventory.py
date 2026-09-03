"""Inventory loading and validation."""

from __future__ import annotations

import ipaddress
import json
import re
from dataclasses import dataclass
from pathlib import Path


_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(?:\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
)


@dataclass(frozen=True, slots=True)
class Device:
    name: str
    host: str
    platform: str = "cisco_ios"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("device name cannot be empty")
        try:
            ipaddress.ip_address(self.host)
        except ValueError:
            if not _HOSTNAME_RE.fullmatch(self.host):
                raise ValueError(f"invalid host: {self.host!r}") from None


def load_inventory(path: Path) -> list[Device]:
    """Load devices from a small, dependency-free JSON inventory."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("inventory root must be a JSON list")
    devices = [Device(**item) for item in payload]
    names = [device.name for device in devices]
    if len(names) != len(set(names)):
        raise ValueError("device names must be unique")
    return devices
