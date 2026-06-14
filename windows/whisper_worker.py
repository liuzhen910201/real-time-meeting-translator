import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel
import time

DEVICE_ID = 18
SAMPLE_RATE = 48000
CHUNK_SECONDS = 3
TEMP_WAV = "chunk.wav"

from pathlib import Path

OUT_TEXT = Path("captions_from_audio.txt")
OUT_TEXT.write_text("", encoding="utf-8")



model = WhisperModel("small", device="cpu", compute_type="int8")

print("Listening from CABLE Output...")
print("Ctrl+C to stop.")

while True:
    audio = sd.rec(
        int(CHUNK_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=DEVICE_ID,
    )
    sd.wait()

    sf.write(TEMP_WAV, audio, SAMPLE_RATE)

    segments, info = model.transcribe(
        TEMP_WAV,
        language="en",
        beam_size=1,
    )

    for segment in segments:
        text = segment.text.strip()
        if text:
            line = f"{time.strftime('%H:%M:%S')} {text}"
            print(line)

            with open(OUT_TEXT, "a", encoding="utf-8") as f:
                f.write(line + "\n")