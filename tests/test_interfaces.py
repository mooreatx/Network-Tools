import pytest

from network_tools.interfaces import generate_interface_commands


def test_generates_inclusive_range() -> None:
    assert generate_interface_commands("set interfaces ge-0/0/", " disable", start=1, stop=2) == [
        "set interfaces ge-0/0/1 disable",
        "set interfaces ge-0/0/2 disable",
    ]


@pytest.mark.parametrize("start,stop", [(-1, 2), (2, -1), (3, 2)])
def test_rejects_invalid_ranges(start: int, stop: int) -> None:
    with pytest.raises(ValueError):
        generate_interface_commands("interface ", "", start=start, stop=stop)
