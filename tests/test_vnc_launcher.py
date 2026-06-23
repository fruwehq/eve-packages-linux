"""Argv parity for the vnc launcher builders (v4.4 §8)."""
from __future__ import annotations

import os

import pytest

from tests.conftest import load_client

rl = load_client("vnc")


@pytest.fixture(autouse=True)
def _scrub_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("VNC_DESKTOP_SIZE",):
        monkeypatch.delenv(key, raising=False)


def test_vnc_tunnel_opts_and_command() -> None:
    assert rl.vnc_tunnel_opts_vagrant("2222", "/k/id") == [
        "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-p", "2222", "-i", "/k/id",
    ]
    assert rl.vnc_tunnel_opts_terraform("/k/id") == [
        "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
        "-o", "ServerAliveInterval=10", "-i", "/k/id",
    ]
    assert rl.vnc_tunnel_opts_terraform("") == [
        "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "ServerAliveInterval=10",
    ]
    assert rl.vnc_tunnel_command("15900", "5901", "ubuntu@1.2.3.4", ["-i", "/k"]) == [
        "ssh", "-f", "-N", "-L", "15900:127.0.0.1:5901", "-i", "/k", "ubuntu@1.2.3.4",
    ]


def test_vnc_viewer_args(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("VNC_DESKTOP_SIZE", raising=False)
    assert rl.vnc_viewer_args() == [
        "-Shared", "-AcceptClipboard", "-SendClipboard", "-RemoteResize=0", "-AlwaysCursor=1", "-CursorType=System",
    ]
    monkeypatch.setenv("VNC_DESKTOP_SIZE", "1920x1080")
    assert rl.vnc_viewer_args()[-2:] == ["-DesktopSize", "1920x1080"]


def test_vncviewer_and_system_commands() -> None:
    assert rl.vncviewer_command(["-Shared"], ["-passwd", "/p"], "15900") == [
        "vncviewer", "-Shared", "-passwd", "/p", "127.0.0.1::15900",
    ]
    assert rl.vnc_system_open_command("vagrant", "15900") == ["open", "vnc://:vagrant@127.0.0.1:15900"]
