"""Argv parity for the rustdesk launcher builders (v4.4 §8)."""
from __future__ import annotations

import os

import pytest

from tests.conftest import load_client

rl = load_client("rustdesk")


def test_rustdesk_connect_command_without_password(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("RUSTDESK_PASSWORD", raising=False)
    assert rl.rustdesk_connect_command("rustdesk", "123456789") == ["rustdesk", "--connect", "123456789"]


def test_rustdesk_connect_command_with_password(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RUSTDESK_PASSWORD", "hunter2")
    assert rl.rustdesk_connect_command("rustdesk", "123456789") == [
        "rustdesk", "--connect", "123456789", "--password", "hunter2",
    ]


def test_shell_quote() -> None:
    assert rl.shell_quote("simple") == "'simple'"
    assert rl.shell_quote("it's") == "'it'\\''s'"
