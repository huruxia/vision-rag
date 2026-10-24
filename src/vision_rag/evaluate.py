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
UNANSWERED = [
    "开心是谁的小猫",
    "今天上海天气怎么样",
    "怎么煮一碗好吃的面条",
]



def recall_at_k(ranked: list[int], gold: int, k: int) -> bool:
    return gold in ranked[:k]

def run_eval() -> None:
    hits1 = hits3 = 0
    mrr_sum = 0.0
    ans_scores = [] #在循环前初始化
    for item in EVAL:
        results = retrieve(item["q"], top_k=3)
        top_score = results[0][0]
        ranked = [r["doc_id"] for _, r in results]
        r1 = recall_at_k(ranked, item["doc_id"], 1)
        r3 = recall_at_k(ranked, item["doc_id"], 3)
        pos = next((i + 1 for i, d in enumerate(ranked) if d == item["doc_id"]), 0)
        mrr = 1.0 / pos if pos else 0.0
        hits1 += int(r1)
        hits3 += int(r3)
        mrr_sum += mrr
        ans_scores.append(top_score)
        print(f"[{item['q'][:12]:<12}] r@1={int(r1)} r@3={int(r3)} mrr={mrr:.2f}  top1=文档{ranked[0]}  分数={top_score:.3f}")
    n = len(EVAL)
    print(f"\n基线: Recall@1={hits1 / n:.2f}  Recall@3={hits3 / n:.2f}  MRR={mrr_sum / n:.2f}  (共{n}题)")
    
    n = len(EVAL)
    print(f"\n有答案卷: Recall@1={hits1 / n:.2f}  Recall@3={hits3 / n:.2f}  MRR={mrr_sum / n:.2f}  (共{n}题)")
    print(f"有答案题 top1 分数范围: {min(ans_scores):.3f} ~ {max(ans_scores):.3f}")

    print("\n--- 无答案卷（观察 top1 分数，找分界线）---")
    for q in UNANSWERED:
        results = retrieve(q, top_k=1)
        print(f"[{q[:12]:<12}] top1分数={results[0][0]:.3f}  命中文档{results[0][1]['doc_id']}")


if __name__ == "__main__":
    run_eval()
