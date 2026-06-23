#!/usr/bin/env python3
"""Sunshine/Moonlight launcher argv builders (ported from core for v4.4 §8).

Pure builders composed by the entry launchers (sunshine-open, sunshine-wait,
moonlight-open, moonlight-pair). moonlight is Sunshine's client, so its
builders live here on the sunshine package.
"""
from __future__ import annotations

import os
import re

_MOONLIGHT_APP = "/Applications/Moonlight.app/Contents/MacOS/Moonlight"

_MOONLIGHT_DISPLAY_MODES = {"fullscreen", "borderless", "windowed"}
_MOONLIGHT_VIDEO_CODECS = {"auto", "H.264", "HEVC", "AV1"}
_MOONLIGHT_VIDEO_DECODERS = {"auto", "hardware", "software"}


def moonlight_stream_command(ip: str) -> list[str]:
    """Build the Moonlight ``stream`` argv from EPHEMERAL_* env knobs.

    Exits 2 on an invalid env value, matching the original core validation.
    """
    cmd = [_MOONLIGHT_APP, "stream", "--game-optimization"]
    res = os.environ.get("EPHEMERAL_DISPLAY_RESOLUTION", "")
    if res:
        cmd += ["--resolution", res]
    fps = os.environ.get("EPHEMERAL_DISPLAY_FPS", "")
    if fps:
        cmd += ["--fps", fps]
    bitrate = os.environ.get("EPHEMERAL_MOONLIGHT_BITRATE_KBPS", "")
    if bitrate:
        cmd += ["--bitrate", bitrate]
    mode = os.environ.get("EPHEMERAL_MOONLIGHT_DISPLAY_MODE", "")
    if mode:
        if mode not in _MOONLIGHT_DISPLAY_MODES:
            print(
                f"moonlight-open: invalid EPHEMERAL_MOONLIGHT_DISPLAY_MODE='{mode}' "
                "(valid: fullscreen, borderless, windowed)",
                flush=True,
            )
            raise SystemExit(2)
        cmd += ["--display-mode", mode]
    codec = os.environ.get("EPHEMERAL_MOONLIGHT_VIDEO_CODEC", "")
    if codec:
        if codec not in _MOONLIGHT_VIDEO_CODECS:
            print(
                f"moonlight-open: invalid EPHEMERAL_MOONLIGHT_VIDEO_CODEC='{codec}' "
                "(valid: auto, H.264, HEVC, AV1)",
                flush=True,
            )
            raise SystemExit(2)
        cmd += ["--video-codec", codec]
    decoder = os.environ.get("EPHEMERAL_MOONLIGHT_VIDEO_DECODER", "")
    if decoder:
        if decoder not in _MOONLIGHT_VIDEO_DECODERS:
            print(
                f"moonlight-open: invalid EPHEMERAL_MOONLIGHT_VIDEO_DECODER='{decoder}' "
                "(valid: auto, hardware, software)",
                flush=True,
            )
            raise SystemExit(2)
        cmd += ["--video-decoder", decoder]
    cmd += [ip, "Desktop"]
    return cmd


def moonlight_pair_command(ip: str, pin: str) -> list[str]:
    return [_MOONLIGHT_APP, "pair", "--pin", pin, ip]


def sunshine_pair_curl_command(ip: str, pin: str, response_file: str) -> list[str]:
    password = os.environ.get("EPHEMERAL_SUNSHINE_PASSWORD", "")
    return [
        "curl", "-sS", "-i", "-k",
        "-u", f"sunshine:{password}",
        "-H", "Content-Type: application/json",
        "--data-binary", f'{{"pin":"{pin}","name":"ephemeral-client"}}',
        "-o", response_file,
        "-w", "%{http_code}",
        f"https://{ip}:47990/api/pin",
    ]


def sunshine_config_curl_command(ip: str) -> list[str]:
    password = os.environ.get("EPHEMERAL_SUNSHINE_PASSWORD", "")
    return [
        "curl", "-sS", "-k", "-L",
        "-u", f"sunshine:{password}",
        "-o", "/dev/null",
        "-w", "%{http_code}",
        f"https://{ip}:47990/api/config",
    ]


_UNIX_USER_RE = re.compile(r"^[a-zA-Z0-9._-]+$")


def validate_unix_user(name: str) -> None:
    if not _UNIX_USER_RE.fullmatch(name):
        print(f"sunshine: unsupported VM user name: {name}", flush=True)
        raise SystemExit(2)
