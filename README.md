# Real-Time Meeting Translator

A lightweight real-time meeting translation system built with:

* VB-CABLE
* OpenAI GPT-4o Mini Transcribe (or Faster-Whisper)
* DeepSeek
* Edge-TTS

The system captures meeting audio directly from the computer, converts speech to text, translates it into another language, and optionally plays the translated result as speech.

---

# Architecture

```text
Teams / Zoom / Browser Meeting
            │
            ▼
      VB-CABLE
            │
            ▼
 Speech-to-Text
 (GPT-4o Mini Transcribe
      or Whisper)
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

# Features

* Real-time speech recognition
* Supports GPT-4o Mini Transcribe
* Supports Faster-Whisper
* DeepSeek translation
* Text-to-speech playback
* Works with Teams, Zoom, Google Meet, browser meetings, etc.
* No dependency on meeting subtitles

---

# Prerequisites

## 1. Install VB-CABLE

Download:

https://vb-audio.com/Cable/

Install:

```text
VBCABLE_Setup_x64.exe
```

Run as Administrator.

After installation, reboot Windows.

You should see:

Output Device:

```text
CABLE Input (VB-Audio Virtual Cable)
```

Input Device:

```text
CABLE Output (VB-Audio Virtual Cable)
```

---

## 2. Configure Teams

Teams Settings

```text
Speaker:
CABLE Input (VB-Audio Virtual Cable)

Microphone:
Realtek Microphone
```

This routes remote participants' audio into VB-CABLE while keeping your microphone unchanged.

---

# Installation

## Python

Recommended:

```bash
pip install sounddevice
pip install soundfile
pip install openai
pip install faster-whisper
pip install edge-tts
```

---

# Environment Variables

## OpenAI

```powershell
$env:OPENAI_API_KEY="your_openai_key"
```

## DeepSeek

```powershell
$env:DEEPSEEK_API_KEY="your_deepseek_key"
```

---

# Files

## whisper_worker.py

Local speech recognition using Faster-Whisper.

Flow:

```text
VB-CABLE
↓
Whisper
↓
captions_from_audio.txt
```

Pros:

* Free
* Fully local

Cons:

* Lower accuracy than GPT-4o Mini Transcribe

---

## gpt_transcribe_worker.py

Speech recognition using OpenAI GPT-4o Mini Transcribe.

Flow:

```text
VB-CABLE
↓
GPT-4o Mini Transcribe
↓
captions_from_audio.txt
```

Pros:

* Higher accuracy
* Better technical terminology recognition

Cons:

* Uses OpenAI API credits

---

## translation_worker.py

Reads recognized text and translates it using DeepSeek.

Flow:

```text
captions_from_audio.txt
↓
DeepSeek
↓
translated.log
↓
latest_translation.txt
```

Features:

* Automatic source language detection
* Configurable target language
* Translation history logging

---

## tts_worker.py

Reads translated text and generates speech.

Flow:

```text
latest_translation.txt
↓
Edge-TTS
↓
Audio Playback
```

Features:

* Chinese voice output
* Automatic playback
* Near real-time speech synthesis

---

# Running

Speech Recognition

Choose one:

```bash
python whisper_worker.py
```

or

```bash
python gpt_transcribe_worker.py
```

Translation

```bash
python translation_worker.py
```

Speech Output

```bash
python tts_worker.py
```

---

# Example Workflow

```text
English Meeting Audio

"How should we migrate this system to AWS?"

↓

Speech Recognition

"How should we migrate this system to AWS?"

↓

DeepSeek Translation

"我们应该如何将该系统迁移到 AWS？"

↓

Edge-TTS

Chinese speech playback
```

---

# Future Improvements

* Streaming transcription
* GPT-4o Realtime API
* Context-aware translation
* Multi-speaker recognition
* Meeting summary generation
* Translation memory
* Custom terminology dictionary
* Lower latency processing

---

# Disclaimer

This project is intended for learning, experimentation, and productivity enhancement purposes.

Please comply with your organization's meeting recording and privacy policies before using it in production environments.
