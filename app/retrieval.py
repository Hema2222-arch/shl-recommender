import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class CatalogRetriever:
    def __init__(self, catalog):
        self.catalog = catalog

    def search(self, query: str, top_k: int = 10):
        q_words = set(query.lower().split())
        scored = []

        for item in self.catalog:
            text = f"{item.get('name','')} {item.get('test_type','')} {item.get('description','')}".lower()
            score = sum(1 for w in q_words if w in text)

            if score > 0:
                result = dict(item)
                result["score"] = score
                scored.append(result)

        scored.sort(key=lambda x: x["score"], reverse=True)

        if not scored:
            return self.catalog[:top_k]

        return scored[:top_k]