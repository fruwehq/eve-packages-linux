#!/usr/bin/env python3
"""Xpra launcher argv builders + helpers (ported from core for v4.4 §8)."""
from __future__ import annotations

from shutil import which


def has_command(name: str) -> bool:
    return which(name) is not None


def ssh_config_field(config: str, field: str) -> str:
    for line in config.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] == field:
            return parts[1]
    return ""


def xpra_ssh_opts(priv_key: str, ssh_port: str) -> list[str]:
    opts = [
        "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=10",
        "-o", "WarnWeakCrypto=no-pq-kex",
    ]
    if priv_key:
        opts += ["-i", priv_key]
    if ssh_port != "22":
        opts += ["-p", ssh_port]
    return opts


def xpra_attach_linux_command(uri: str, ssh_cmd: str) -> list[str]:
    return ["xpra", "attach", uri, f"--ssh={ssh_cmd}", "--clipboard=yes"]


def xpra_attach_windows_command(uri: str) -> list[str]:
    return ["xpra", "attach", uri, "--desktop-fullscreen=yes", "--clipboard=yes"]


def xpra_attach_desktop_command(uri: str, ssh_cmd: str) -> list[str]:
    return [
        "xpra", "attach", uri, f"--ssh={ssh_cmd}",
        "--desktop-fullscreen=no", "--desktop-scaling=1", "--clipboard=yes",
    ]


def xpra_tunnel_command(tcp_port: str, ssh_opts: list[str], ssh_user: str, ip: str) -> list[str]:
    return [
        "ssh", *ssh_opts, "-l", ssh_user, "-N",
        "-L", f"{tcp_port}:127.0.0.1:{tcp_port}", ip,
    ]
