from __future__ import annotations

import logging
import os
import platform
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT_DIR / "config.yaml"


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def load_config(config_path: str | Path = DEFAULT_CONFIG) -> dict[str, Any]:
    path = Path(config_path)
    if not path.is_absolute():
        path = ROOT_DIR / path
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    import yaml

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def project_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT_DIR / path


def require_env(name: str, purpose: str) -> str:
    value = os.getenv(name)
    if value:
        value = value.strip()
    if not value:
        raise RuntimeError(
            f"Missing {name}. Set it before starting {purpose}. "
            f"Example: export {name}=your_key_here"
        )
    return value


def timestamp() -> str:
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def append_line(path: str | Path, text: str) -> None:
    file_path = project_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("a", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")


def read_lines(path: str | Path) -> list[str]:
    file_path = project_path(path)
    if not file_path.exists():
        return []
    return file_path.read_text(encoding="utf-8").splitlines()


def write_text(path: str | Path, text: str) -> None:
    file_path = project_path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(text, encoding="utf-8")


def clear_runtime_files(config: dict[str, Any]) -> None:
    files = config.get("files", {})
    for key in ("captions_file", "translated_log", "latest_translation"):
        path = files.get(key)
        if path:
            write_text(path, "")


def log_startup(config: dict[str, Any], mode: str, tts_enabled: bool) -> None:
    audio = config.get("audio", {})
    logging.info("Selected mode: %s", mode)
    logging.info("OS platform: %s", platform.platform())
    logging.info("Audio device id: %s", audio.get("device_id"))
    logging.info("Chunk seconds: %s", audio.get("chunk_seconds"))
    logging.info("TTS enabled: %s", tts_enabled)
