from __future__ import annotations

import argparse
import logging
import re
import time
from typing import Any

from openai import OpenAI

from .utils import DEFAULT_CONFIG, append_line, load_config, read_lines, require_env, write_text


TIMESTAMP_RE = re.compile(r"^\[[^\]]+\]\s*")


def strip_timestamp(line: str) -> str:
    return TIMESTAMP_RE.sub("", line).strip()


def build_prompt(target_language: str) -> str:
    return f"""You are a professional simultaneous interpreter.

Detect the source language automatically.

Translate the text into {target_language}.

Rules:
- Keep the original meaning.
- Use natural spoken language.
- Correct obvious speech recognition errors when the context is clear.
- Do not explain.
- Do not summarize.
- Output translation only."""


def translate_text(client: OpenAI, model: str, target_language: str, text: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": build_prompt(target_language)},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
    )
    return (response.choices[0].message.content or "").strip()


def run(config: dict[str, Any]) -> None:
    api_key = require_env("DEEPSEEK_API_KEY", "DeepSeek translation")
    translation = config.get("translation", {})
    files = config.get("files", {})
    model = translation.get("model", "deepseek-chat")
    target_language = translation.get("target_language", "Chinese")
    buffer_lines = int(translation.get("buffer_lines", 2))
    check_interval = float(translation.get("check_interval", 0.1))
    captions_file = files.get("captions_file", "captions_from_audio.txt")
    latest_translation = files.get("latest_translation", "latest_translation.txt")
    translated_log = files.get("translated_log", "translated.log")

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    processed_count = 0
    logging.info(
        "DeepSeek translation started with model=%s target=%s buffer_lines=%s",
        model,
        target_language,
        buffer_lines,
    )

    while True:
        try:
            lines = [line for line in read_lines(captions_file) if line.strip()]
            if len(lines) > processed_count:
                end = len(lines)
                start = max(processed_count, end - buffer_lines)
                text = "\n".join(strip_timestamp(line) for line in lines[start:end])
                result = translate_text(client, model, target_language, text)
                if result:
                    write_text(latest_translation, result)
                    append_line(translated_log, result)
                    logging.info("Translation result: %s", result)
                processed_count = end
            time.sleep(check_interval)
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            logging.error("Translation error: %s", exc)
            time.sleep(1.0)


def main() -> None:
    parser = argparse.ArgumentParser(description="DeepSeek translation worker")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()
    run(load_config(args.config))


if __name__ == "__main__":
    main()
