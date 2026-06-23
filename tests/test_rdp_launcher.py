"""Argv parity for the rdp launcher builders (v4.4 §8)."""
from __future__ import annotations

from tests.conftest import load_client

rl = load_client("rdp")


def test_rdp_file_lines() -> None:
    assert rl.rdp_file_lines("10.0.0.5", "Administrator", 1, 0, 1) == [
        "full address:s:10.0.0.5",
        "username:s:Administrator",
        "prompt for credentials on client:i:1",
        "enablecredsspsupport:i:1",
        "use redirection server name:i:0",
        "administrative session:i:1",
        "screen mode id:i:2",
        "session bpp:i:32",
        "redirectclipboard:i:1",
        "audiomode:i:0",
    ]


def test_xfreerdp_command() -> None:
    assert rl.xfreerdp_command("10.0.0.5", "user", "pw", ["/gfx:AVC444"]) == [
        "xfreerdp", "/v:10.0.0.5", "/u:user", "/p:pw", "+clipboard", "/cert:ignore", "/gfx:AVC444",
    ]


def test_msrdp_open_and_paste_commands() -> None:
    assert rl.msrdp_open_command("tmp/windows.rdp") == ["open", "-a", "Microsoft Remote Desktop", "tmp/windows.rdp"]
    assert rl.msrdp_paste_command()[0] == "osascript"
    assert "key code 36" in rl.msrdp_paste_command()[-1]
