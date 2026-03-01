import json
from pathlib import Path


# Resolve path to configs/ai_sources.json
BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = BASE_DIR / "configs" / "ai_sources.json"


def load_sources():
    """
    Load AI source configuration from JSON file.
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def print_sources(config):
    """
    Pretty-print loaded sources (for sanity check).
    """
    sources = config.get("sources", [])
    print(f"\nLoaded {len(sources)} AI sources:\n")

    for idx, src in enumerate(sources, start=1):
        print(f"{idx}. {src['name']} ({src['type']})")
        print(f"   URL: {src['url']}")
        print(f"   Trust score: {src['trust_score']}\n")


if __name__ == "__main__":
    config = load_sources()
    print(f"Niche: {config['niche']}")
    print(f"Description: {config['description']}")
    print_sources(config)