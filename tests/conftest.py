"""Pytest setup for eve-packages-linux launcher parity tests (v4.4 §8).

Loads a package's command-builder module (commands/_client.py) by file path, so
the tests can assert argv parity without making each package a Python package.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent


def load_client(package: str) -> Any:
    path = REPO / package / "commands" / "_client.py"
    spec = importlib.util.spec_from_file_location(f"{package}._client", str(path))
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
