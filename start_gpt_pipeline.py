import subprocess
import time

print("Starting GPT Meeting Translator...")

processes = []

processes.append(
subprocess.Popen(
["python", "gpt_transcribe_worker.py"]
)
)

time.sleep(2)

processes.append(
subprocess.Popen(
["python", "translation_worker.py"]
)
)

time.sleep(2)

processes.append(
subprocess.Popen(
["python", "tts_worker.py"]
)
)

print("All workers started.")
print("Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:


    print("Stopping workers...")

    for p in processes:
        p.terminate()

