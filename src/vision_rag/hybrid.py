import json
from .bm25 import BM25
from .embed import embed
from .retrieve import cos_sim

def search(query: str, top_k: int = 3) -> list[tuple[float, dict]]:
    with open("data/index/v0.json", encoding="utf-8") as f:
        index = json.load(f)

    # 通道 1：向量检索（语义）
    qvec = embed(query)
    vec = [cos_sim(qvec, item["vector"]) for item in index]

    # 通道 2：BM25（关键词，本地计算 0 成本）
    bm = BM25([item["text"] for item in index])
    bm25 = bm.scores(query)

    # RRF 融合：不看量纲，只看名次
    rrf = [0.0] * len(index)
    pool = 2 * top_k                                 # 每通道前 2×top_k 进决赛
    for scores in (vec, bm25):
        order = sorted(range(len(index)), key=lambda i: scores[i], reverse=True)[:pool]
        for rank, i in enumerate(order):
            rrf[i] += 1.0 / (60 + rank + 1)

    final = sorted(range(len(index)), key=lambda i: rrf[i], reverse=True)[:top_k]
    return [(vec[i], index[i]) for i in final]   # 排序用 RRF，分数保留向量余弦（置信度语义）

