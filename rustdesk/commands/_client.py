#!/usr/bin/env python3
"""RustDesk launcher argv builders (ported from core for v4.4 §8)."""
from __future__ import annotations

import os
import platform
from shutil import which

_RUSTDESK_APP = "/Applications/RustDesk.app/Contents/MacOS/rustdesk"


def rustdesk_local_client() -> str:
    if platform.system() == "Darwin":
        if os.access(_RUSTDESK_APP, os.X_OK):
            return _RUSTDESK_APP
    for candidate in ("rustdesk", "/usr/bin/rustdesk"):
        if which(candidate) is not None or os.access(candidate, os.X_OK):
            return candidate
    return ""


def rustdesk_connect_command(cli: str, rustdesk_id: str) -> list[str]:
    cmd = [cli, "--connect", rustdesk_id]
    password = os.environ.get("RUSTDESK_PASSWORD", "")
    if password:
        cmd += ["--password", password]
    return cmd


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\\''") + "'"
