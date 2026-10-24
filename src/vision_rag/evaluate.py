from .retrieve import retrieve

EVAL = [
    {"q": "什么是RAG", "doc_id": 0},
    {"q": "RAG怎么让模型不瞎编", "doc_id": 0},
    {"q": "RAG的关键指标有哪些", "doc_id": 0},
    {"q": "什么是嵌入", "doc_id": 1},
    {"q": "余弦相似度是什么", "doc_id": 1},
    {"q": "怎么算两个向量的相似度", "doc_id": 1},
    {"q": "什么是智能体", "doc_id": 2},
    {"q": "智能体的循环是怎样的", "doc_id": 2},
    {"q": "为什么要分块", "doc_id": 3},
    {"q": "分块大小怎么选", "doc_id": 3},
]

def recall_at_k(ranked: list[int], gold: int, k: int) -> bool:
    return gold in ranked[:k]

def run_eval() -> None:
    hits1 = hits3 = 0
    mrr_sum = 0.0
    for item in EVAL:
        results = retrieve(item["q"], top_k=3)
        ranked = [r["doc_id"] for _, r in results]
        r1 = recall_at_k(ranked, item["doc_id"], 1)
        r3 = recall_at_k(ranked, item["doc_id"], 3)
        pos = next((i + 1 for i, d in enumerate(ranked) if d == item["doc_id"]), 0)
        mrr = 1.0 / pos if pos else 0.0
        hits1 += int(r1)
        hits3 += int(r3)
        mrr_sum += mrr
        print(f"[{item['q'][:12]:<12}] r@1={int(r1)} r@3={int(r3)} mrr={mrr:.2f}  top1=文档{ranked[0]}")
    n = len(EVAL)
    print(f"\n基线: Recall@1={hits1 / n:.2f}  Recall@3={hits3 / n:.2f}  MRR={mrr_sum / n:.2f}  (共{n}题)")

if __name__ == "__main__":
    run_eval()
