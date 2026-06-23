"""Argv parity for the xpra launcher builders (v4.4 §8)."""
from __future__ import annotations

from tests.conftest import load_client

rl = load_client("xpra")


def test_xpra_ssh_opts() -> None:
    assert rl.xpra_ssh_opts("/k/id", "2222") == [
        "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=10",
        "-o", "WarnWeakCrypto=no-pq-kex", "-i", "/k/id", "-p", "2222",
    ]
    assert rl.xpra_ssh_opts("", "22") == [
        "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=10", "-o", "WarnWeakCrypto=no-pq-kex",
    ]


def test_xpra_attach_commands() -> None:
    assert rl.xpra_attach_linux_command("ssh://u@h/100", "ssh -o X=y") == [
        "xpra", "attach", "ssh://u@h/100", "--ssh=ssh -o X=y", "--clipboard=yes",
    ]
    assert rl.xpra_attach_windows_command("tcp://localhost:14500") == [
        "xpra", "attach", "tcp://localhost:14500", "--desktop-fullscreen=yes", "--clipboard=yes",
    ]
    assert rl.xpra_attach_desktop_command("ssh://u@h/101", "ssh -o X=y") == [
        "xpra", "attach", "ssh://u@h/101", "--ssh=ssh -o X=y",
        "--desktop-fullscreen=no", "--desktop-scaling=1", "--clipboard=yes",
    ]
    assert rl.xpra_tunnel_command("14500", ["-o", "X=y"], "Administrator", "1.2.3.4") == [
        "ssh", "-o", "X=y", "-l", "Administrator", "-N", "-L", "14500:127.0.0.1:14500", "1.2.3.4",
    ]
