"""Argv parity for the thinlinc launcher builders (v4.4 §8)."""
from __future__ import annotations

import os

import pytest

from tests.conftest import load_client

rl = load_client("thinlinc")


def test_thinlinc_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("THINLINC_WEBACCESS_PORT", raising=False)
    assert rl.thinlinc_url("10.0.0.5") == "https://10.0.0.5:300"
    monkeypatch.setenv("THINLINC_WEBACCESS_PORT", "443")
    assert rl.thinlinc_url("10.0.0.5") == "https://10.0.0.5:443"


def test_thinlinc_client_args_and_commands() -> None:
    assert rl.thinlinc_client_args("10.0.0.5", "eve") == ["-u", "eve", "10.0.0.5"]
    assert rl.thinlinc_client_args("10.0.0.5", "") == ["10.0.0.5"]
    assert rl.thinlinc_client_macos_command(["-u", "eve", "1.2.3.4"]) == [
        "open", "-a", "ThinLinc Client", "--args", "-u", "eve", "1.2.3.4",
    ]
    assert rl.thinlinc_client_linux_command(["-u", "eve", "1.2.3.4"]) == ["tlclient", "-u", "eve", "1.2.3.4"]


def test_url_open_command() -> None:
    assert rl.url_open_command("open", "https://x:300") == ["open", "https://x:300"]
