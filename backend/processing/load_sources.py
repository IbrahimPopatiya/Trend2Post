import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / "configs" / "ai_sources.json"

def load_sources():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    sources = load_sources()
    print(f"Loaded {len(sources['sources'])} AI sources")
    for src in sources["sources"]:
        print("-", src["name"])