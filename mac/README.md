# Real-Time Meeting Translator

Real-Time Meeting Translator captures meeting audio from a virtual audio device, transcribes speech, translates it with DeepSeek, and optionally plays translated speech with Edge-TTS.

Recommended stable mode:

```bash
python start_pipeline.py --mode gpt
```

Local/free fallback mode:

```bash
python start_pipeline.py --mode whisper
```

## Architecture

```text
Teams / Zoom / Browser Meeting
        -> virtual audio device
        -> GPT or faster-whisper transcription
        -> captions_from_audio.txt
        -> DeepSeek translation
        -> latest_translation.txt / translated.log
        -> Edge-TTS playback
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## API Keys

Use environment variables. Do not put API keys in source files.

macOS / Linux:

```bash
export OPENAI_API_KEY="your_openai_key"
export DEEPSEEK_API_KEY="your_deepseek_key"
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_openai_key"
$env:DEEPSEEK_API_KEY="your_deepseek_key"
```

`OPENAI_API_KEY` is required for GPT transcription. `DEEPSEEK_API_KEY` is required for translation.

## Configuration

Edit `config.yaml`:

```yaml
audio:
  device_id: null
  sample_rate: 48000
  chunk_seconds: 2.0
```

Set `audio.device_id` to the virtual input device shown by:

```bash
python -m src.audio_capture --list-devices
```

Do not hard-code device names. Device IDs are different on each computer.

## Startup

GPT transcription + DeepSeek translation + Edge-TTS:

```bash
python start_pipeline.py --mode gpt
```

Whisper transcription + DeepSeek translation + Edge-TTS:

```bash
python start_pipeline.py --mode whisper
```

Disable TTS:

```bash
python start_pipeline.py --mode gpt --no-tts
```

At startup, the pipeline clears:

```text
captions_from_audio.txt
translated.log
latest_translation.txt
```

This prevents old meeting text from affecting a new session.

## Windows Audio Setup: VB-CABLE

Install VB-CABLE.

Typical devices:

```text
Output: CABLE Input (VB-Audio Virtual Cable)
Input:  CABLE Output (VB-Audio Virtual Cable)
```

Set the meeting app speaker to:

```text
CABLE Input
```

Set `audio.device_id` in `config.yaml` to the ID for:

```text
CABLE Output
```

Use the device list command to find the correct ID.

TTS playback on Windows uses PowerShell `System.Windows.Media.MediaPlayer`.

## macOS Audio Setup: BlackHole

Install BlackHole 2ch.

Open Audio MIDI Setup and create a Multi-Output Device that includes:

```text
BlackHole 2ch
Real speaker / headphones
```

Set the meeting app speaker to:

```text
Multi-Output Device
```

Set `audio.device_id` in `config.yaml` to the ID for:

```text
BlackHole 2ch
```

TTS playback on macOS uses `afplay`.

## Teams / Zoom / Browser Settings

In the meeting app, set the speaker/output device to the virtual audio output path:

Windows:

```text
CABLE Input
```

macOS:

```text
Multi-Output Device
```

Python captures from the corresponding virtual input device configured by `audio.device_id`.

The project does not require Teams subtitles or Zoom captions.

## Files

```text
start_pipeline.py              unified startup
config.yaml                    runtime configuration
src/audio_capture.py           sounddevice capture and device listing
src/transcribe_gpt.py          OpenAI GPT transcription
src/transcribe_whisper.py      faster-whisper transcription
src/translator.py              DeepSeek translation
src/tts.py                     Edge-TTS generation and playback
src/pipeline.py                process orchestration
src/vad_segmenter.py           placeholder for future VAD support
captions_from_audio.txt        timestamped transcription output
latest_translation.txt         latest translated text for TTS
translated.log                 translation history
```

Legacy wrapper scripts remain:

```text
gpt_transcribe_worker.py
whisper_worker.py
translation_worker.py
tts_worker.py
start_gpt_pipeline.py
```

## VAD Future Work

The current stable pipeline records fixed-size chunks using `audio.chunk_seconds`.

Future VAD segmentation can detect speech start, record while speech continues, detect silence, and submit a complete utterance to transcription. This should improve transcription accuracy, translation quality, TTS naturalness, and latency balance.

Candidate libraries:

```text
silero-vad
webrtcvad
```

## Known Limitations

- Device IDs vary by machine and must be configured manually.
- GPT mode requires internet access and `OPENAI_API_KEY`.
- Translation requires internet access and `DEEPSEEK_API_KEY`.
- Whisper mode is local for transcription, but translation still uses DeepSeek.
- Linux playback is best-effort and needs `ffplay`, `mpg123`, or `mpv`.
- Fixed-size audio chunks may split sentences until VAD is implemented.
