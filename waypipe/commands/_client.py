#!/usr/bin/env python3
"""Waypipe launcher argv builders (ported from core for v4.4 §8)."""
from __future__ import annotations


def waypipe_vagrant_command(ssh_config: str, app: list[str]) -> list[str]:
    return [
        "waypipe", "ssh", "-o", "StreamLocalBindUnlink=yes", "-F", ssh_config, "default", *app,
    ]


def waypipe_ssh_command(ssh_opts: list[str], target: str, app: list[str]) -> list[str]:
    return ["waypipe", "ssh", *ssh_opts, target, *app]


def waypipe_ssh_opts(priv_key: str) -> list[str]:
    opts = [
        "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=10",
        "-o", "WarnWeakCrypto=no-pq-kex", "-o", "StreamLocalBindUnlink=yes",
    ]
    if priv_key:
        opts += ["-i", priv_key, "-o", "IdentitiesOnly=yes"]
    return opts
