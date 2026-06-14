from __future__ import annotations

from typing import Any


class VadSegmenter:
    """Placeholder for future VAD-based utterance segmentation.

    The current stable pipeline records fixed-size chunks from the configured
    audio device. A future implementation can replace fixed chunking with:
    detect speech start, record while speaking, detect silence, then submit one
    utterance to transcription.

    VAD should improve transcription accuracy, translation quality, TTS
    naturalness, and latency balance by sending complete spoken phrases instead
    of arbitrary time slices.

    Candidate libraries:
    - silero-vad
    - webrtcvad
    """

    def __init__(self, config: dict[str, Any]):
        self.config = config

    def enabled(self) -> bool:
        return False
