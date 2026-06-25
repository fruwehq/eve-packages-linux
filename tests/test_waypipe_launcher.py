"""Argv parity for the waypipe launcher builders (v4.4 §8)."""
from __future__ import annotations

from tests.conftest import load_client

rl = load_client("waypipe")


def test_waypipe_commands() -> None:
    assert rl.waypipe_vagrant_command("/tmp/cfg", ["foot"]) == [
        "waypipe", "ssh", "-o", "StreamLocalBindUnlink=yes", "-F", "/tmp/cfg", "default", "foot",
    ]
    assert rl.waypipe_ssh_command(["-o", "X=y"], "ubuntu@1.2.3.4", ["foot"]) == [
        "waypipe", "ssh", "-o", "X=y", "ubuntu@1.2.3.4", "foot",
    ]
    assert rl.waypipe_ssh_opts("/k/id") == [
        "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=10",
        "-o", "WarnWeakCrypto=no-pq-kex", "-o", "StreamLocalBindUnlink=yes",
        "-i", "/k/id", "-o", "IdentitiesOnly=yes",
    ]
    assert rl.waypipe_ssh_opts("") == [
        "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=10",
        "-o", "WarnWeakCrypto=no-pq-kex", "-o", "StreamLocalBindUnlink=yes",
    ]
