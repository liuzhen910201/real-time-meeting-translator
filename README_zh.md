# 实时会议翻译系统

一个基于 VB-CABLE、OpenAI、DeepSeek 和 Edge-TTS 构建的实时会议翻译系统。

该系统能够直接获取电脑中的会议声音，将语音转换为文字，翻译为目标语言，并自动进行语音播报。

支持：

* Microsoft Teams
* Zoom
* Google Meet
* 浏览器会议
* 其他电脑音频来源

无需依赖会议软件自带字幕。

---

# 系统架构

```text
会议声音
(Teams / Zoom)

        ↓

VB-CABLE 虚拟声卡

        ↓

语音识别
(Whisper 或 GPT-4o Mini Transcribe)

        ↓

captions_from_audio.txt

        ↓

DeepSeek 翻译

        ↓

latest_translation.txt

        ↓

Edge-TTS

        ↓

中文语音播放
```

---

# 功能特点

* 实时语音识别
* 实时翻译
* 实时语音播报
* 支持 GPT-4o Mini Transcribe
* 支持 Faster-Whisper
* 不依赖 Teams 字幕
* 可扩展为实时同声传译系统

---

# 环境准备

## 安装 VB-CABLE

下载地址：

https://vb-audio.com/Cable/

下载后运行：

```text
VBCABLE_Setup_x64.exe
```

以管理员身份安装。

安装完成后重启电脑。

---

## 验证安装

安装成功后应看到：

输出设备：

```text
CABLE Input
(VB-Audio Virtual Cable)
```

输入设备：

```text
CABLE Output
(VB-Audio Virtual Cable)
```

---

# Teams 配置

Teams 设置：

```text
扬声器：
CABLE Input

麦克风：
Realtek Microphone
```

这样：

* 对方声音进入 VB-CABLE
* 自己麦克风保持正常

---

# Python 依赖安装

```bash
pip install sounddevice
pip install soundfile
pip install openai
pip install faster-whisper
pip install edge-tts
```

---

# API Key 配置

## OpenAI

用于 GPT-4o Mini Transcribe

PowerShell：

```powershell
$env:OPENAI_API_KEY="你的OpenAIKey"
```

---

## DeepSeek

用于翻译

PowerShell：

```powershell
$env:DEEPSEEK_API_KEY="你的DeepSeekKey"
```

---

# 文件说明

## whisper_worker.py

本地语音识别模块。

工作流程：

```text
VB-CABLE
↓
Whisper
↓
captions_from_audio.txt
```

特点：

* 免费
* 本地运行
* 不消耗 API

缺点：

* 准确率略低

---

## gpt_transcribe_worker.py

OpenAI GPT-4o Mini Transcribe 版本。

工作流程：

```text
VB-CABLE
↓
GPT-4o Mini Transcribe
↓
captions_from_audio.txt
```

特点：

* 准确率更高
* 技术术语识别更好
* 更适合会议场景

缺点：

* 消耗 OpenAI API 额度

---

## translation_worker.py

翻译模块。

工作流程：

```text
captions_from_audio.txt
↓
DeepSeek
↓
translated.log
↓
latest_translation.txt
```

功能：

* 自动识别源语言
* 翻译为目标语言
* 保存翻译历史

---

## tts_worker.py

语音播报模块。

工作流程：

```text
latest_translation.txt
↓
Edge-TTS
↓
自动播放
```

功能：

* 中文语音播报
* 自动监听翻译结果
* 自动播放最新翻译

---

# 运行方式

## 方案一：Whisper 版本

终端1：

```bash
python whisper_worker.py
```

终端2：

```bash
python translation_worker.py
```

终端3：

```bash
python tts_worker.py
```

---

## 方案二：GPT-4o Mini Transcribe 版本

终端1：

```bash
python gpt_transcribe_worker.py
```

终端2：

```bash
python translation_worker.py
```

终端3：

```bash
python tts_worker.py
```

---

# 示例流程

英文会议：

```text
How should we migrate this system to AWS?
```

↓

语音识别：

```text
How should we migrate this system to AWS?
```

↓

DeepSeek 翻译：

```text
我们应该如何将该系统迁移到 AWS？
```

↓

Edge-TTS 播报：

```text
我们应该如何将该系统迁移到 AWS？
```

---

# 已知问题

目前版本主要用于验证整体流程。

可能存在：

* 识别延迟
* 技术术语识别错误
* 多人同时说话时识别准确率下降
* TTS 播报延迟

---

# 后续优化方向

* GPT-4o Realtime API
* 流式语音识别
* 上下文感知翻译
* 术语词典
* 会议纪要自动生成
* 多说话人识别
* 降低整体延迟
* 支持更多语言

---

# 项目目标

实现一个低成本、可扩展、可本地部署的实时会议翻译系统。

在保证准确率的前提下，尽可能降低延迟，提高会议沟通效率。
