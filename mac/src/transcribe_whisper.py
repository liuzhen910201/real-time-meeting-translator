from __future__ import annotations

import argparse
import logging
import time
from typing import Any

from faster_whisper import WhisperModel

from .audio_capture import record_chunk
from .utils import DEFAULT_CONFIG, append_line, load_config, timestamp


def run(config: dict[str, Any]) -> None:
    transcription = config.get("transcription", {})
    model_name = transcription.get("whisper_model", "small")
    device = transcription.get("whisper_device", "cpu")
    compute_type = transcription.get("whisper_compute_type", "int8")
    captions_file = config.get("files", {}).get("captions_file", "captions_from_audio.txt")

    logging.info(
        "Whisper transcription started with model=%s device=%s compute_type=%s",
        model_name,
        device,
        compute_type,
    )
    model = WhisperModel(model_name, device=device, compute_type=compute_type)

    while True:
        try:
            audio_path = record_chunk(config)
            segments, _ = model.transcribe(str(audio_path), vad_filter=False)
            text = " ".join(segment.text.strip() for segment in segments).strip()
            if text:
                line = f"[{timestamp()}] {text}"
                append_line(captions_file, line)
                logging.info("Transcription result: %s", text)
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            logging.error("Whisper transcription error: %s", exc)
            time.sleep(1.0)


def main() -> None:
    parser = argparse.ArgumentParser(description="faster-whisper transcription worker")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()
    run(load_config(args.config))


if __name__ == "__main__":
    main()
