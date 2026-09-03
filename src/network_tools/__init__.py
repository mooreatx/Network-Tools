"""Reusable network automation utilities."""

from network_tools.interfaces import generate_interface_commands
from network_tools.mac import MacAddress

__all__ = ["MacAddress", "generate_interface_commands"]
__version__ = "1.0.0"
