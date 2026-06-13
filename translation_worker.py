
import os
import time
from pathlib import Path

from openai import OpenAI


# ==========================
# 配置
# ==========================

CAPTION_FILE = Path("captions_from_audio.txt")

TRANSLATED_LOG = Path("translated.log")

LATEST_FILE = Path("latest_translation.txt")

BUFFER_LINES = 2

CHECK_INTERVAL = 0.1

TARGET_LANGUAGE = "Chinese"


# ==========================
# DeepSeek
# ==========================

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# ==========================
# 工具函数
# ==========================

def read_new_lines(path, last_position):
    with open(path, "r", encoding="utf-8") as f:
        f.seek(last_position)

        lines = f.readlines()

        new_position = f.tell()

    return lines, new_position


def translate_text(text):

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": f"""
You are a professional simultaneous interpreter.

Detect the source language automatically.

Translate the text into {TARGET_LANGUAGE}.

Rules:
- Keep the original meaning.
- Use natural spoken language.
- Output translation only.
"""
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


def append_translation(original, translated):

    with open(
        TRANSLATED_LOG,
        "a",
        encoding="utf-8"
    ) as f:

        f.write("=" * 80 + "\n")

        f.write("ORIGINAL\n")
        f.write(original + "\n\n")

        f.write("TRANSLATED\n")
        f.write(translated + "\n\n")


def write_latest(translated):

    with open(
        LATEST_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(translated)


# ==========================
# 主程序
# ==========================

def main():

    print("translation_worker started")

    TRANSLATED_LOG.write_text("", encoding="utf-8")
    LATEST_FILE.write_text("", encoding="utf-8")

    if not CAPTION_FILE.exists():
        print("captions_from_audio.txt not found")
        return

    last_position = 0

    buffer = []

    while True:

        try:

            lines, last_position = read_new_lines(
                CAPTION_FILE,
                last_position
            )

            for line in lines:

                line = line.strip()

                if not line:
                    continue

                # 去掉时间戳
                if len(line) > 9 and line[2] == ":" and line[5] == ":":
                    line = line[9:]

                buffer.append(line)

            if len(buffer) >= BUFFER_LINES:

                text_to_translate = "\n".join(buffer)

                print("\n====================")
                print("TRANSLATING")
                print("====================")

                print(text_to_translate)

                translated = translate_text(
                    text_to_translate
                )

                print("\nRESULT\n")
                print(translated)

                append_translation(
                    text_to_translate,
                    translated
                )

                write_latest(
                    translated
                )

                buffer = []

            time.sleep(CHECK_INTERVAL)

        except Exception as e:

            print("ERROR:", e)

            time.sleep(5)


if __name__ == "__main__":
    main()

