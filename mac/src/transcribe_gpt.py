from __future__ import annotations

import argparse
import logging
import time
from typing import Any

from openai import OpenAI

from .audio_capture import record_chunk
from .utils import DEFAULT_CONFIG, append_line, load_config, require_env, timestamp


def transcribe_file(client: OpenAI, audio_path, model: str) -> str:
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(model=model, file=audio_file)
    return (getattr(result, "text", "") or "").strip()


def run(config: dict[str, Any]) -> None:
    require_env("OPENAI_API_KEY", "GPT transcription")
    client = OpenAI()
    model = config.get("transcription", {}).get("gpt_model", "gpt-4o-mini-transcribe")
    captions_file = config.get("files", {}).get("captions_file", "captions_from_audio.txt")
    logging.info("GPT transcription started with model: %s", model)

    while True:
        try:
            audio_path = record_chunk(config)
            text = transcribe_file(client, audio_path, model)
            if text:
                line = f"[{timestamp()}] {text}"
                append_line(captions_file, line)
                logging.info("Transcription result: %s", text)
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            logging.error("GPT transcription error: %s", exc)
            time.sleep(1.0)


def main() -> None:
    parser = argparse.ArgumentParser(description="GPT transcription worker")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()
    run(load_config(args.config))


if __name__ == "__main__":
    main()
