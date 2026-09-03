import pytest

from network_tools.mac import MacAddress


@pytest.mark.parametrize(
    "value",
    ["00:11:22:aa:bb:cc", "00-11-22-AA-BB-CC", "0011.22aa.bbcc", "001122aabbcc"],
)
def test_formats_supported_inputs(value: str) -> None:
    mac = MacAddress(value)
    assert mac.colon == "00:11:22:aa:bb:cc"
    assert mac.hyphen == "00-11-22-aa-bb-cc"
    assert mac.cisco == "0011.22aa.bbcc"


@pytest.mark.parametrize("value", ["", "0011", "00:11:22:33:44:gg", "00 11 22 33 44 55"])
def test_rejects_invalid_addresses(value: str) -> None:
    with pytest.raises(ValueError):
        MacAddress(value)
