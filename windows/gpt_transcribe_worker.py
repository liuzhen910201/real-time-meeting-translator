import os
import time
from pathlib import Path

import sounddevice as sd
import soundfile as sf
from openai import OpenAI

# ==========================

# Config

# ==========================

DEVICE_ID = 18

SAMPLE_RATE = 48000

CHUNK_SECONDS = 2

TEMP_WAV = "chunk.wav"

OUT_TEXT = Path("captions_from_audio.txt")

OUT_TEXT.write_text("", encoding="utf-8")

# ==========================

# OpenAI

# ==========================

client = OpenAI(
api_key=os.getenv("OPENAI_API_KEY")
)

# ==========================

# Main

# ==========================

print("GPT Transcribe Worker Started")
print(f"Device: {DEVICE_ID}")
print("Ctrl+C to stop")

while True:


    try:

        audio = sd.rec(
            int(CHUNK_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=DEVICE_ID,
        )

        sd.wait()

        sf.write(
            TEMP_WAV,
            audio,
            SAMPLE_RATE
        )

        with open(TEMP_WAV, "rb") as audio_file:

            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        text = transcript.text.strip()

        if text:

            line = f"{time.strftime('%H:%M:%S')} {text}"

            print(line)

            with open(
                OUT_TEXT,
                "a",
                encoding="utf-8"
            ) as f:

                f.write(line + "\n")

    except KeyboardInterrupt:

        print("Stopped")
        break

    except Exception as e:

        print("ERROR:", e)

        time.sleep(1)

