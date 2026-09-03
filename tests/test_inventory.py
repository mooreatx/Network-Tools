import json

import pytest

from network_tools.inventory import Device, load_inventory


def test_accepts_ip_or_hostname() -> None:
    assert Device("edge-1", "192.0.2.10").host == "192.0.2.10"
    assert Device("edge-2", "edge-2.example.net").host == "edge-2.example.net"


def test_rejects_invalid_host() -> None:
    with pytest.raises(ValueError, match="invalid host"):
        Device("bad", "not a host!")


def test_loads_inventory(tmp_path) -> None:
    path = tmp_path / "inventory.json"
    path.write_text(json.dumps([{"name": "lab", "host": "192.0.2.1"}]), encoding="utf-8")
    assert load_inventory(path) == [Device("lab", "192.0.2.1")]


def test_rejects_duplicate_names(tmp_path) -> None:
    path = tmp_path / "inventory.json"
    path.write_text(
        json.dumps(
            [
                {"name": "lab", "host": "192.0.2.1"},
                {"name": "lab", "host": "192.0.2.2"},
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unique"):
        load_inventory(path)


def test_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="name"):
        Device("", "192.0.2.1")


def test_rejects_non_list_inventory(tmp_path) -> None:
    path = tmp_path / "inventory.json"
    path.write_text('{"name": "lab"}', encoding="utf-8")
    with pytest.raises(ValueError, match="JSON list"):
        load_inventory(path)
