from src.pipeline import run_pipeline
from src.utils import DEFAULT_CONFIG, load_config


if __name__ == "__main__":
    run_pipeline(load_config(DEFAULT_CONFIG), mode="gpt", no_tts=False)
