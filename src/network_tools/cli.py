"""Command-line entry point."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
import json

from network_tools.interfaces import generate_interface_commands
from network_tools.mac import MacAddress
from network_tools.reachability import ping_many


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="network-tools",
        description="Safe network engineering utilities",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    mac_parser = subparsers.add_parser("mac", help="normalize a MAC address")
    mac_parser.add_argument("address")
    mac_parser.add_argument(
        "--format",
        choices=("plain", "colon", "hyphen", "cisco", "json"),
        default="json",
    )

    interface_parser = subparsers.add_parser(
        "interfaces",
        help="generate an interface command range",
    )
    interface_parser.add_argument("prefix")
    interface_parser.add_argument("suffix")
    interface_parser.add_argument("--start", type=int, default=0)
    interface_parser.add_argument("--stop", type=int, default=47)

    ping_parser = subparsers.add_parser("ping", help="check target reachability")
    ping_parser.add_argument("targets", nargs="+")
    ping_parser.add_argument("--count", type=int, default=2)
    ping_parser.add_argument("--timeout", type=int, default=2)
    ping_parser.add_argument("--workers", type=int, default=10)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "mac":
        formats = MacAddress(args.address).as_dict()
        print(json.dumps(formats, indent=2) if args.format == "json" else formats[args.format])
        return 0
    if args.command == "interfaces":
        commands = generate_interface_commands(
            args.prefix,
            args.suffix,
            start=args.start,
            stop=args.stop,
        )
        print("\n".join(commands))
        return 0
    results = ping_many(
        args.targets,
        count=args.count,
        timeout=args.timeout,
        workers=args.workers,
    )
    payload = [
        {
            "target": result.target,
            "reachable": result.reachable,
            "return_code": result.return_code,
        }
        for result in results
    ]
    print(json.dumps(payload, indent=2))
    return 0 if all(result.reachable for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
