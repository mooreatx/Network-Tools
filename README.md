# Network Automation Tools

[![CI](https://github.com/mooreatx/Network-Tools/actions/workflows/ci.yml/badge.svg)]
(https://github.com/mooreatx/Network-Tools/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-minded Python toolkit that turns common network-engineering tasks into reusable,
tested components. It demonstrates validation, concurrent reachability checks, vendor-aware
automation boundaries, dependency injection, typed data models, and continuous integration.

## Highlights

- Convert MAC addresses among IEEE, Cisco, Windows, and plain formats.
- Generate deterministic Junos or IOS interface command ranges.
- Check multiple endpoints concurrently without shell injection risks.
- Load validated device inventories using documentation-only sample networks.
- Collect Cisco IOS facts and perform explicit configuration operations through Netmiko.
- Test device workflows without connecting to real hardware.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'

network-tools mac 0011.2233.4455
network-tools interfaces 'set interfaces ge-0/0/' ' disable' --start 0 --stop 3
network-tools ping 1.1.1.1 example.com
pytest
```

Install the optional device-automation dependency with:

```bash
python -m pip install -e '.[automation]'
```

## Python API

```python
from network_tools import MacAddress, generate_interface_commands

print(MacAddress("00:11:22:aa:bb:cc").cisco)
commands = generate_interface_commands(
    "set interfaces ge-0/0/",
    " unit 0 family ethernet-switching",
    start=0,
    stop=3,
)
```

Device credentials are supplied at runtime and are never read from inventory files:

```python
import getpass
from pathlib import Path

from network_tools.inventory import load_inventory
from network_tools.netmiko_ops import collect_facts

device = load_inventory(Path("inventory.json"))[0]
username = input("Username: ")
password = getpass.getpass("Password: ")
facts = collect_facts(device, username, password)
```

## Project layout

```text
src/network_tools/      Installable application package
tests/                  Unit tests, including mocked device sessions
examples/               Sanitized example inventory
.github/workflows/      Multi-version lint and test pipeline
```

## Safety model

Configuration changes are isolated in named functions and receive targets explicitly. The project
does not embed credentials, production addresses, or automatic host-key acceptance. Example IPs use
the RFC 5737 documentation range. Run configuration changes in a lab first and use a least-privilege
account.

## Roadmap

- Add structured TextFSM/Genie parsing for collected facts.
- Add Nornir inventory and task-runner integration.
- Add containerlab-based integration tests for multi-vendor workflows.
- Export Prometheus-compatible reachability metrics.

## License

MIT
