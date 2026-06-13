# Real-Time Meeting Translator

A real-time meeting translation system built with:

* VB-CABLE
* OpenAI GPT-4o Mini Transcribe
* Faster-Whisper
* DeepSeek
* Edge-TTS

The system captures meeting audio directly from the computer, converts speech to text, translates it into another language, and optionally plays the translated result as speech.

---

# Current Pipeline

```text
Teams / Zoom / Browser Meeting
            │
            ▼
      VB-CABLE
            │
            ▼
 Speech-to-Text

 Option A:
 GPT-4o Mini Transcribe

 Option B:
 Faster-Whisper

            │
            ▼
captions_from_audio.txt
            │
            ▼
 DeepSeek Translation
            │
            ▼
latest_translation.txt
            │
            ▼
      Edge-TTS
            │
            ▼
     Audio Playback
```

---

# Implemented Features

✅ System audio capture via VB-CABLE

✅ GPT-4o Mini Transcribe support

✅ Faster-Whisper support

✅ DeepSeek translation

✅ Automatic speech playback

✅ One-command startup

✅ No dependency on Teams subtitles

---

# Project Structure

```text
gpt_transcribe_worker.py
    Speech-to-text using OpenAI

whisper_worker.py
    Speech-to-text using Faster-Whisper

translation_worker.py
    Translation using DeepSeek

tts_worker.py
    Speech synthesis using Edge-TTS

start_gpt_pipeline.py
    Start all workers automatically
```

---

# Quick Start

Configure API Keys:

```powershell
$env:OPENAI_API_KEY="your_openai_key"

$env:DEEPSEEK_API_KEY="your_deepseek_key"
```

Run:

```bash
python start_gpt_pipeline.py
```

This automatically starts:

* gpt_transcribe_worker.py
* translation_worker.py
* tts_worker.py

---

# Available Modes

## GPT Mode (Recommended)

```bash
python start_gpt_pipeline.py
```

Advantages:

* Higher transcription accuracy
* Better technical terminology recognition
* Better meeting experience

Requires OpenAI API credits.

---

## Whisper Mode

```bash
python whisper_worker.py
python translation_worker.py
python tts_worker.py
```

Advantages:

* Completely local
* No transcription cost

Lower accuracy than GPT-4o Mini Transcribe.

```
```
