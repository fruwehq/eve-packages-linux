#!/usr/bin/env python3
"""RDP launcher argv builders (ported from core for v4.4 §8)."""
from __future__ import annotations


def rdp_file_lines(
    ip: str, username: str, credssp: int, redirect: int, admin_session: int,
) -> list[str]:
    return [
        f"full address:s:{ip}",
        f"username:s:{username}",
        "prompt for credentials on client:i:1",
        f"enablecredsspsupport:i:{credssp}",
        f"use redirection server name:i:{redirect}",
        f"administrative session:i:{admin_session}",
        "screen mode id:i:2",
        "session bpp:i:32",
        "redirectclipboard:i:1",
        "audiomode:i:0",
    ]


def xfreerdp_command(ip: str, username: str, password: str, extra: list[str]) -> list[str]:
    return [
        "xfreerdp", f"/v:{ip}", f"/u:{username}", f"/p:{password}",
        "+clipboard", "/cert:ignore", *extra,
    ]


def msrdp_open_command(rdp_file: str) -> list[str]:
    return ["open", "-a", "Microsoft Remote Desktop", rdp_file]


def msrdp_paste_command() -> list[str]:
    return [
        "osascript",
        "-e", 'tell application "System Events" to keystroke "v" using command down',
        "-e", 'tell application "System Events" to key code 36',
    ]
