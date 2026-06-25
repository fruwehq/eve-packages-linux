"""Argv parity for the sunshine/moonlight launcher builders (v4.4 §8)."""
from __future__ import annotations

import os

import pytest

from tests.conftest import load_client

rl = load_client("sunshine")


@pytest.fixture(autouse=True)
def _scrub_ephemeral_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in list(os.environ):
        if key.startswith("EPHEMERAL_"):
            monkeypatch.delenv(key, raising=False)


def test_moonlight_stream_command_base() -> None:
    assert rl.moonlight_stream_command("10.0.0.5") == [
        "/Applications/Moonlight.app/Contents/MacOS/Moonlight", "stream",
        "--game-optimization", "10.0.0.5", "Desktop",
    ]


def test_moonlight_stream_command_with_env_knobs(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EPHEMERAL_DISPLAY_RESOLUTION", "2560x1440")
    monkeypatch.setenv("EPHEMERAL_DISPLAY_FPS", "120")
    monkeypatch.setenv("EPHEMERAL_MOONLIGHT_BITRATE_KBPS", "50000")
    monkeypatch.setenv("EPHEMERAL_MOONLIGHT_DISPLAY_MODE", "borderless")
    monkeypatch.setenv("EPHEMERAL_MOONLIGHT_VIDEO_CODEC", "HEVC")
    monkeypatch.setenv("EPHEMERAL_MOONLIGHT_VIDEO_DECODER", "hardware")
    assert rl.moonlight_stream_command("10.0.0.5") == [
        "/Applications/Moonlight.app/Contents/MacOS/Moonlight", "stream",
        "--game-optimization",
        "--resolution", "2560x1440", "--fps", "120", "--bitrate", "50000",
        "--display-mode", "borderless", "--video-codec", "HEVC", "--video-decoder", "hardware",
        "10.0.0.5", "Desktop",
    ]


@pytest.mark.parametrize(
    "env_var, value",
    [
        ("EPHEMERAL_MOONLIGHT_DISPLAY_MODE", "weird"),
        ("EPHEMERAL_MOONLIGHT_VIDEO_CODEC", "MPEG2"),
        ("EPHEMERAL_MOONLIGHT_VIDEO_DECODER", "quantum"),
    ],
)
def test_moonlight_invalid_env_exits_2(env_var: str, value: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(env_var, value)
    with pytest.raises(SystemExit) as exc:
        rl.moonlight_stream_command("1.2.3.4")
    assert exc.value.code == 2


def test_moonlight_pair_command() -> None:
    assert rl.moonlight_pair_command("10.0.0.5", "1234") == [
        "/Applications/Moonlight.app/Contents/MacOS/Moonlight", "pair", "--pin", "1234", "10.0.0.5",
    ]


def test_sunshine_pair_curl_command(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EPHEMERAL_SUNSHINE_PASSWORD", "s3cret")
    assert rl.sunshine_pair_curl_command("10.0.0.5", "1234", "/tmp/r.json") == [
        "curl", "-sS", "-i", "-k", "-u", "sunshine:s3cret",
        "-H", "Content-Type: application/json",
        "--data-binary", '{"pin":"1234","name":"ephemeral-client"}',
        "-o", "/tmp/r.json", "-w", "%{http_code}", "https://10.0.0.5:47990/api/pin",
    ]


def test_sunshine_config_curl_command(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EPHEMERAL_SUNSHINE_PASSWORD", "pw")
    assert rl.sunshine_config_curl_command("10.0.0.5") == [
        "curl", "-sS", "-k", "-L", "-u", "sunshine:pw",
        "-o", "/dev/null", "-w", "%{http_code}", "https://10.0.0.5:47990/api/config",
    ]
