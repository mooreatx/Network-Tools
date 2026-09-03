"""MAC address parsing and formatting."""

from __future__ import annotations

from dataclasses import dataclass
import re


_HEX_RE = re.compile(r"^[0-9a-fA-F]{12}$")


@dataclass(frozen=True, slots=True)
class MacAddress:
    """A validated 48-bit MAC address with vendor-neutral formatters."""

    value: str

    def __post_init__(self) -> None:
        normalized = re.sub(r"[:.\-]", "", self.value).lower()
        if not _HEX_RE.fullmatch(normalized):
            raise ValueError(
                "MAC address must contain exactly 12 hexadecimal characters"
            )
        object.__setattr__(self, "value", normalized)

    @property
    def colon(self) -> str:
        """Return IEEE/EUI-48 colon notation."""
        return ":".join(self.value[index : index + 2] for index in range(0, 12, 2))

    @property
    def hyphen(self) -> str:
        """Return Windows-style hyphen notation."""
        return self.colon.replace(":", "-")

    @property
    def cisco(self) -> str:
        """Return Cisco dotted notation."""
        return ".".join(self.value[index : index + 4] for index in range(0, 12, 4))

    def as_dict(self) -> dict[str, str]:
        """Return every supported representation."""
        return {
            "plain": self.value,
            "colon": self.colon,
            "hyphen": self.hyphen,
            "cisco": self.cisco,
        }
