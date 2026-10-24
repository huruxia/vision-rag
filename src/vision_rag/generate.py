from .llm import chat
from .retrieve import retrieve

THRESHOLD = 0.45 # 检索置信度阈值：top1 分数低于此值 → 判定资料里没有答案

def answer(question: str) -> str:
    results = retrieve(question, top_k=3)
    if results[0][0] < THRESHOLD:        # ← L1 系统层闸门
        return "不知道，我的资料里没有这个信息。"
    context = "\n\n".join(item["text"] for _, item in results)
    prompt = f"""请基于以下资料回答用户问题。如果资料里没有答案，请直接说不知道。

资料：
{context}

问题：{question}"""
    return chat(prompt, temperature=0.5)
