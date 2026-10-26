from .llm import chat
from .hybrid import search as coarse_search
from .rerank import rerank

THRESHOLD = 0.45 # 检索置信度阈值：top1 分数低于此值 → 判定资料里没有答案

def answer(question: str) -> str:
    results = coarse_search(question, top_k=6)   # ① 粗排：BM25+向量捞 6 个
    results = rerank(question, results)[:3]      # ② 精排：LLM 法官重排，取 top3
    if results[0][0] < THRESHOLD:                # ③ 闸门：top1 余弦 < 0.45 → 拒答
        return "不知道，我的资料里没有这个信息。"
    context = "\n\n".join(item["text"] for _, item in results)
    prompt = f"""请基于以下资料回答用户问题。如果资料里没有答案，请直接说不知道。

资料：
{context}

问题：{question}"""
    return chat(prompt, temperature=0.5)
