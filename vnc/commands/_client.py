#!/usr/bin/env python3
"""VNC launcher argv builders + shared helpers (ported from core for v4.4 §8)."""
from __future__ import annotations

import os
import re
from shutil import which

_UNIX_USER_RE = re.compile(r"^[a-zA-Z0-9._-]+$")


def validate_unix_user(name: str) -> None:
    if not _UNIX_USER_RE.fullmatch(name):
        print(f"vnc: unsupported VM user name: {name}", flush=True)
        raise SystemExit(2)


def has_command(name: str) -> bool:
    return which(name) is not None


def ssh_config_field(config: str, field: str) -> str:
    for line in config.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0] == field:
            return parts[1]
    return ""


def vnc_tunnel_command(local_port: str, vnc_port: str, target: str, opts: list[str]) -> list[str]:
    return ["ssh", "-f", "-N", "-L", f"{local_port}:127.0.0.1:{vnc_port}", *opts, target]


def vnc_tunnel_opts_vagrant(ssh_port: str, priv_key: str) -> list[str]:
    return [
        "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
        "-p", ssh_port, "-i", priv_key,
    ]


def vnc_tunnel_opts_terraform(priv_key: str) -> list[str]:
    opts = [
        "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
        "-o", "ServerAliveInterval=10",
    ]
    if priv_key:
        opts += ["-i", priv_key]
    return opts


def vnc_viewer_args() -> list[str]:
    args = [
        "-Shared", "-AcceptClipboard", "-SendClipboard",
        "-RemoteResize=0", "-AlwaysCursor=1", "-CursorType=System",
    ]
    desktop_size = os.environ.get("VNC_DESKTOP_SIZE", "")
    if desktop_size:
        args += ["-DesktopSize", desktop_size]
    return args


def vncviewer_command(viewer_args: list[str], auth_args: list[str], local_port: str) -> list[str]:
    return ["vncviewer", *viewer_args, *auth_args, f"127.0.0.1::{local_port}"]


def vnc_system_open_command(password: str, local_port: str) -> list[str]:
    return ["open", f"vnc://:{password}@127.0.0.1:{local_port}"]


def vnc_passwd_fetch_command(vnc_user: str) -> str:
    return (
        f'home=$(getent passwd \'{vnc_user}\' | cut -d: -f6); '
        'if [ -f "$home/.config/tigervnc/passwd" ]; then '
        'sudo cat "$home/.config/tigervnc/passwd"; '
        'elif [ -f "$home/.vnc/passwd" ]; then '
        'sudo cat "$home/.vnc/passwd"; else exit 1; fi'
    )
