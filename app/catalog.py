import json
from pathlib import Path

CATALOG_PATH = Path("data/catalog.json")


def load_catalog():
    if not CATALOG_PATH.exists():
        raise FileNotFoundError("data/catalog.json not found. Run scraper first.")
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)