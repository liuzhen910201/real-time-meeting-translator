from __future__ import annotations

import argparse
import asyncio
import logging
import platform
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

import edge_tts

from .utils import DEFAULT_CONFIG, load_config, project_path


async def synthesize(text: str, output_path: Path, voice: str, rate: str, volume: str) -> None:
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
    await communicate.save(str(output_path))


def play_audio(path: Path) -> str:
    system = platform.system()
    if system == "Darwin" and shutil.which("afplay"):
        subprocess.run(["afplay", str(path)], check=True)
        return "played with afplay"
    if system == "Windows":
        command = (
            "Add-Type -AssemblyName presentationCore; "
            f"$p=New-Object System.Windows.Media.MediaPlayer; "
            f"$p.Open([Uri]'{path.resolve().as_uri()}'); "
            "$p.Play(); "
            "while($p.NaturalDuration.HasTimeSpan -eq $false){Start-Sleep -Milliseconds 100}; "
            "$d=$p.NaturalDuration.TimeSpan.TotalMilliseconds; "
            "Start-Sleep -Milliseconds ([Math]::Ceiling($d)+300); "
            "$p.Close()"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", command], check=True)
        return "played with PowerShell MediaPlayer"
    for player in ("ffplay", "mpg123", "mpv"):
        if shutil.which(player):
            if player == "ffplay":
                subprocess.run([player, "-nodisp", "-autoexit", str(path)], check=True)
            else:
                subprocess.run([player, str(path)], check=True)
            return f"played with {player}"
    raise RuntimeError(
        "No supported audio player found. macOS uses afplay; Windows uses PowerShell "
        "MediaPlayer; Linux needs ffplay, mpg123, or mpv."
    )


def run(config: dict[str, Any]) -> None:
    tts = config.get("tts", {})
    files = config.get("files", {})
    latest_translation = project_path(files.get("latest_translation", "latest_translation.txt"))
    output_mp3 = project_path(files.get("tts_mp3", "tts_latest.mp3"))
    voice = tts.get("voice", "zh-CN-XiaoxiaoNeural")
    rate = tts.get("rate", "+0%")
    volume = tts.get("volume", "+0%")
    check_interval = float(tts.get("check_interval", 0.2))
    last_text = ""
    logging.info("Edge-TTS started with voice=%s", voice)

    while True:
        try:
            text = latest_translation.read_text(encoding="utf-8").strip() if latest_translation.exists() else ""
            if text and text != last_text:
                asyncio.run(synthesize(text, output_mp3, voice, rate, volume))
                result = play_audio(output_mp3)
                logging.info("TTS playback result: %s", result)
                last_text = text
            time.sleep(check_interval)
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            logging.error("TTS error: %s", exc)
            time.sleep(1.0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Edge-TTS worker")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()
    run(load_config(args.config))


if __name__ == "__main__":
    main()
