import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class CatalogRetriever:
    def __init__(self, catalog):
        self.catalog = catalog
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        texts = [
            f"{item['name']} {item.get('test_type', '')} {item.get('description', '')}"
            for item in catalog
        ]

        self.embeddings = self.model.encode(texts, normalize_embeddings=True)
        self.index = faiss.IndexFlatIP(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings).astype("float32"))

    def search(self, query: str, top_k: int = 10):
        q = self.model.encode([query], normalize_embeddings=True)
        scores, ids = self.index.search(np.array(q).astype("float32"), top_k)

        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx >= 0:
                item = dict(self.catalog[idx])
                item["score"] = float(score)
                results.append(item)

        return results