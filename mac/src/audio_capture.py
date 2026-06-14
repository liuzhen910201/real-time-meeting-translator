from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Any

from .utils import DEFAULT_CONFIG, load_config, project_path


def list_devices() -> None:
    import sounddevice as sd

    print(sd.query_devices())


def record_chunk(config: dict[str, Any], output_path: str | Path | None = None) -> Path:
    audio = config.get("audio", {})
    files = config.get("files", {})
    sample_rate = int(audio.get("sample_rate", 48000))
    chunk_seconds = float(audio.get("chunk_seconds", 2.0))
    device_id = audio.get("device_id")
    temp_wav = project_path(output_path or files.get("temp_wav", "chunk.wav"))
    frames = int(sample_rate * chunk_seconds)

    import sounddevice as sd
    import soundfile as sf

    logging.debug("Recording %.2fs from device %s", chunk_seconds, device_id)
    data = sd.rec(
        frames,
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        device=device_id,
    )
    sd.wait()
    sf.write(temp_wav, data, sample_rate)
    return temp_wav


def main() -> None:
    parser = argparse.ArgumentParser(description="Audio capture helpers")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--list-devices", action="store_true")
    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    config = load_config(args.config)
    path = record_chunk(config)
    print(f"Recorded test chunk: {path}")


if __name__ == "__main__":
    main()
