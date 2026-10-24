import json
import math
from .embed import embed

def cos_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb)

def retrieve(query: str, top_k: int = 3) -> list[tuple[float, dict]]:
    qvec = embed(query)
    with open("data/index/v0.json", encoding="utf-8") as f:
        index = json.load(f)
    scored = [(cos_sim(qvec, item["vector"]), item) for item in index]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]
