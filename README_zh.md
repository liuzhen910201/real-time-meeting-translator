# 实时会议翻译系统

一个基于 VB-CABLE、OpenAI GPT-4o Mini Transcribe、DeepSeek 和 Edge-TTS 的实时会议翻译系统。

系统能够直接获取电脑中的会议声音，进行语音识别、翻译以及语音播报。

无需依赖 Teams 字幕。

---

# 当前架构

```text
Teams / Zoom / 浏览器会议
            │
            ▼
      VB-CABLE
            │
            ▼
      语音转文字

方案一：
GPT-4o Mini Transcribe

方案二：
Faster-Whisper

            │
            ▼
captions_from_audio.txt
            │
            ▼
DeepSeek 翻译
            │
            ▼
latest_translation.txt
            │
            ▼
Edge-TTS
            │
            ▼
中文语音播报
```

---

# 已实现功能

✅ 通过 VB-CABLE 获取会议声音

✅ GPT-4o Mini Transcribe 识别

✅ Faster-Whisper 识别

✅ DeepSeek 翻译

✅ 中文语音播报

✅ 一键启动全部服务

✅ 不依赖 Teams 字幕

---

# 项目结构

```text
gpt_transcribe_worker.py
    OpenAI 语音识别

whisper_worker.py
    Faster-Whisper 本地识别

translation_worker.py
    DeepSeek 翻译

tts_worker.py
    Edge-TTS 语音播报

start_gpt_pipeline.py
    一键启动所有服务
```

---

# 快速开始

配置 API Key：

```powershell
$env:OPENAI_API_KEY="你的OpenAI Key"

$env:DEEPSEEK_API_KEY="你的DeepSeek Key"
```

启动：

```bash
python start_gpt_pipeline.py
```

系统将自动启动：

* gpt_transcribe_worker.py
* translation_worker.py
* tts_worker.py

---

# 两种运行模式

## GPT 模式（推荐）

```bash
python start_gpt_pipeline.py
```

优点：

* 识别准确率更高
* 技术术语识别更好
* 更适合会议场景

缺点：

* 消耗 OpenAI API 额度

---

## Whisper 模式

```bash
python whisper_worker.py
python translation_worker.py
python tts_worker.py
```

优点：

* 完全本地运行
* 无识别成本

缺点：

* 准确率低于 GPT-4o Mini Transcribe

---

# 项目目标

构建一个低成本、可扩展、可本地部署的实时会议同声传译系统。

未来计划：

* VAD 自动切句
* GPT-4o Realtime API
* 上下文翻译
* 多说话人识别
* 自动会议纪要
* 专业术语词典
* 更低延迟

```
```
