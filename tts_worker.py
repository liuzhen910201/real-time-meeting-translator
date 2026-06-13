import asyncio
import time
import subprocess
from pathlib import Path

import edge_tts


LATEST_FILE = Path("latest_translation.txt")
TTS_MP3 = Path("tts_latest.mp3")

CHECK_INTERVAL = 0.3

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+0%"
VOLUME = "+0%"


async def make_tts(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE,
        volume=VOLUME,
    )
    await communicate.save(str(TTS_MP3))


def play_mp3(path):
    ps_script = f"""
Add-Type -AssemblyName PresentationCore
$player = New-Object System.Windows.Media.MediaPlayer
$player.Open([uri]'{path.resolve().as_uri()}')
$player.Play()
Start-Sleep -Milliseconds 300
while ($player.NaturalDuration.HasTimeSpan -eq $false) {{
    Start-Sleep -Milliseconds 100
}}
$duration = $player.NaturalDuration.TimeSpan.TotalMilliseconds
Start-Sleep -Milliseconds ([int]$duration + 300)
$player.Close()
"""

    subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def read_latest():
    if not LATEST_FILE.exists():
        return ""

    return LATEST_FILE.read_text(encoding="utf-8").strip()


def main():
    print("tts_worker started")
    print("Watching latest_translation.txt")
    print("Ctrl+C to stop.")

    last_text = ""

    while True:
        try:
            text = read_latest()

            if text and text != last_text:
                last_text = text

                print("\nSPEAKING:")
                print(text)

                asyncio.run(make_tts(text))
                play_mp3(TTS_MP3)

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("tts_worker stopped")
            break

        except Exception as e:
            print("ERROR:", e)
            time.sleep(1)


if __name__ == "__main__":
    main()