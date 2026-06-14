# 实时会议翻译器

实时会议翻译器会从虚拟声卡采集会议声音，进行语音识别，用 DeepSeek 翻译，并可选用 Edge-TTS 播放翻译后的语音。

推荐稳定模式：

```bash
python start_pipeline.py --mode gpt
```

本地/免费备用模式：

```bash
python start_pipeline.py --mode whisper
```

## 架构

```text
Teams / Zoom / 浏览器会议
        -> 虚拟音频设备
        -> GPT 或 faster-whisper 语音识别
        -> captions_from_audio.txt
        -> DeepSeek 翻译
        -> latest_translation.txt / translated.log
        -> Edge-TTS 播放
```

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## API Key

请使用环境变量，不要把 API Key 写进代码。

macOS / Linux：

```bash
export OPENAI_API_KEY="your_openai_key"
export DEEPSEEK_API_KEY="your_deepseek_key"
```

Windows PowerShell：

```powershell
$env:OPENAI_API_KEY="your_openai_key"
$env:DEEPSEEK_API_KEY="your_deepseek_key"
```

GPT 识别需要 `OPENAI_API_KEY`。DeepSeek 翻译需要 `DEEPSEEK_API_KEY`。

## 配置

编辑 `config.yaml`：

```yaml
audio:
  device_id: null
  sample_rate: 48000
  chunk_seconds: 2.0
```

用下面的命令查看音频设备：

```bash
python -m src.audio_capture --list-devices
```

把 `audio.device_id` 设置为虚拟输入设备的 ID。不要硬编码设备名称，因为每台电脑的设备 ID 都可能不同。

## 启动

GPT 识别 + DeepSeek 翻译 + Edge-TTS：

```bash
python start_pipeline.py --mode gpt
```

Whisper 识别 + DeepSeek 翻译 + Edge-TTS：

```bash
python start_pipeline.py --mode whisper
```

关闭 TTS：

```bash
python start_pipeline.py --mode gpt --no-tts
```

每次启动时会清空：

```text
captions_from_audio.txt
translated.log
latest_translation.txt
```

这样可以避免上一次会议内容影响新会议。

## Windows 音频设置：VB-CABLE

安装 VB-CABLE。

常见设备名称：

```text
输出：CABLE Input (VB-Audio Virtual Cable)
输入：CABLE Output (VB-Audio Virtual Cable)
```

会议软件的扬声器设置为：

```text
CABLE Input
```

`config.yaml` 里的 `audio.device_id` 设置为这个设备的 ID：

```text
CABLE Output
```

请用设备列表命令查找正确 ID。

Windows 上 TTS 播放使用 PowerShell 的 `System.Windows.Media.MediaPlayer`。

## macOS 音频设置：BlackHole

安装 BlackHole 2ch。

打开“音频 MIDI 设置”，创建一个 Multi-Output Device，包含：

```text
BlackHole 2ch
真实扬声器 / 耳机
```

会议软件的扬声器设置为：

```text
Multi-Output Device
```

`config.yaml` 里的 `audio.device_id` 设置为这个设备的 ID：

```text
BlackHole 2ch
```

macOS 上 TTS 播放使用 `afplay`。

## Teams / Zoom / 浏览器设置

在会议软件中，把扬声器/输出设备设置为虚拟音频输出路径：

Windows：

```text
CABLE Input
```

macOS：

```text
Multi-Output Device
```

Python 会从 `audio.device_id` 配置的虚拟输入设备采集声音。

本项目不需要 Teams 字幕，也不依赖 Zoom 字幕。

## 文件说明

```text
start_pipeline.py              统一启动入口
config.yaml                    运行配置
src/audio_capture.py           sounddevice 采集和设备列表
src/transcribe_gpt.py          OpenAI GPT 语音识别
src/transcribe_whisper.py      faster-whisper 语音识别
src/translator.py              DeepSeek 翻译
src/tts.py                     Edge-TTS 生成和播放
src/pipeline.py                多进程编排
src/vad_segmenter.py           未来 VAD 支持占位
captions_from_audio.txt        带时间戳的识别结果
latest_translation.txt         最新翻译结果，供 TTS 读取
translated.log                 翻译历史
```

保留了旧脚本包装入口：

```text
gpt_transcribe_worker.py
whisper_worker.py
translation_worker.py
tts_worker.py
start_gpt_pipeline.py
```

## VAD 后续计划

当前稳定版本使用 `audio.chunk_seconds` 固定时长切分音频。

后续可以加入 VAD：检测开始说话，持续录音直到静音，然后把完整句段提交给语音识别。这样可以改善识别准确率、翻译质量、TTS 自然度，以及延迟平衡。

候选库：

```text
silero-vad
webrtcvad
```

## 已知限制

- 音频设备 ID 每台机器不同，需要手动配置。
- GPT 模式需要网络和 `OPENAI_API_KEY`。
- 翻译需要网络和 `DEEPSEEK_API_KEY`。
- Whisper 模式的语音识别是本地的，但翻译仍使用 DeepSeek。
- Linux 播放是尽力支持，需要 `ffplay`、`mpg123` 或 `mpv`。
- 当前固定时长切分可能切断句子，后续 VAD 会改善。
