#!/usr/bin/env python3
"""ThinLinc launcher argv builders (ported from core for v4.4 §8)."""
from __future__ import annotations

import os
from shutil import which


def thinlinc_url(ip: str) -> str:
    port = os.environ.get("THINLINC_WEBACCESS_PORT", "300")
    return f"https://{ip}:{port}"


def thinlinc_client_args(ip: str, user_name: str) -> list[str]:
    args: list[str] = []
    if user_name:
        args += ["-u", user_name]
    args.append(ip)
    return args


def thinlinc_client_macos_command(args: list[str]) -> list[str]:
    return ["open", "-a", "ThinLinc Client", "--args", *args]


def thinlinc_client_linux_command(args: list[str]) -> list[str]:
    return ["tlclient", *args]


def url_open_command(opener: str, url: str) -> list[str]:
    return [opener, url]


def has_command(name: str) -> bool:
    return which(name) is not None
