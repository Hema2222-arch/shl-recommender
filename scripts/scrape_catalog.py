import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"


def scrape_catalog():
    items = []

    for page in range(1, 20):
        url = f"{CATALOG_URL}?start={page * 12}"
        html = requests.get(url, timeout=20).text
        soup = BeautifulSoup(html, "html.parser")

        links = soup.select("a[href*='/solutions/products/product-catalog/view/']")
        if not links:
            break

        for link in links:
            name = link.get_text(strip=True)
            href = urljoin(BASE_URL, link["href"])

            if not name:
                continue

            detail_html = requests.get(href, timeout=20).text
            detail_soup = BeautifulSoup(detail_html, "html.parser")
            text = detail_soup.get_text(" ", strip=True)

            test_type = infer_test_type(text)

            item = {
                "name": name,
                "url": href,
                "test_type": test_type,
                "description": text[:3000]
            }

            if item not in items:
                items.append(item)

    with open("data/catalog.json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(items)} catalog items")


def infer_test_type(text: str) -> str:
    lowered = text.lower()

    if "personality" in lowered or "opq" in lowered:
        return "P"
    if "cognitive" in lowered or "ability" in lowered:
        return "A"
    if "knowledge" in lowered or "java" in lowered or "python" in lowered:
        return "K"
    if "situational" in lowered or "judgement" in lowered:
        return "S"

    return "Other"


if __name__ == "__main__":
    scrape_catalog()