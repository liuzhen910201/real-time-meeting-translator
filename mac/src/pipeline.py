from __future__ import annotations

import argparse
import logging
import multiprocessing as mp
import os
import signal
from typing import Any

from .utils import DEFAULT_CONFIG, clear_runtime_files, load_config, log_startup, setup_logging


def worker_entry(name: str, target, config: dict[str, Any]) -> None:
    setup_logging()
    try:
        target(config)
    except KeyboardInterrupt:
        logging.info("%s stopped", name)


def check_environment(selected_mode: str) -> None:
    required = ["DEEPSEEK_API_KEY"]
    if selected_mode == "gpt":
        required.append("OPENAI_API_KEY")

    missing = [name for name in required if not (os.getenv(name) or "").strip()]
    if missing:
        formatted = ", ".join(missing)
        raise RuntimeError(
            f"Missing environment variable(s): {formatted}. "
            "Set them in your shell before running the pipeline."
        )


def run_pipeline(config: dict[str, Any], mode: str | None = None, no_tts: bool = False) -> None:
    setup_logging()
    selected_mode = mode or config.get("transcription", {}).get("mode", "gpt")
    if selected_mode not in {"gpt", "whisper"}:
        raise ValueError("mode must be 'gpt' or 'whisper'")

    tts_enabled = bool(config.get("tts", {}).get("enabled", True)) and not no_tts
    check_environment(selected_mode)
    clear_runtime_files(config)
    log_startup(config, selected_mode, tts_enabled)

    from . import translator

    if selected_mode == "gpt":
        from . import transcribe_gpt

        transcription_target = transcribe_gpt.run
    else:
        from . import transcribe_whisper

        transcription_target = transcribe_whisper.run

    workers: list[mp.Process] = [
        mp.Process(target=worker_entry, args=("transcription", transcription_target, config)),
        mp.Process(target=worker_entry, args=("translation", translator.run, config)),
    ]
    if tts_enabled:
        from . import tts

        workers.append(mp.Process(target=worker_entry, args=("tts", tts.run, config)))

    for process in workers:
        process.start()

    def stop_workers(*_args) -> None:
        logging.info("Stopping pipeline...")
        for process in workers:
            if process.is_alive():
                process.terminate()

    signal.signal(signal.SIGINT, stop_workers)
    signal.signal(signal.SIGTERM, stop_workers)

    try:
        for process in workers:
            process.join()
    finally:
        stop_workers()
        for process in workers:
            process.join(timeout=2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Start real-time meeting translator")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--mode", choices=["gpt", "whisper"], default=None)
    parser.add_argument("--no-tts", action="store_true")
    args = parser.parse_args()
    run_pipeline(load_config(args.config), mode=args.mode, no_tts=args.no_tts)


if __name__ == "__main__":
    main()
