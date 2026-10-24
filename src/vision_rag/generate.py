from .llm import chat
from .retrieve import retrieve

def answer(question: str) -> str:
    results = retrieve(question, top_k=3)
    context = "\n\n".join(item["text"] for _, item in results)
    prompt = f"""请基于以下资料回答用户问题。如果资料里没有答案，请直接说不知道。

资料：
{context}

问题：{question}"""
    return chat(prompt, temperature=0.5)
