from .llm import chat

JUDGE_PROMPT = """你是RAG系统的忠实度裁判。给定"资料片段"和"模型回答"，判断回答是否忠实于资料。

规则：
1. 回答中的所有事实陈述，必须能在资料片段中找到依据。
2. 回答如果明确说"不知道/资料中没有"，视为忠实。
3. 资料内容的同义改写、合理推论，不视为新增结论。
4. 只有资料中完全没有依据的新事实（具体数字、人物、事件、因果关系），才视为不忠实。

资料片段：
{context}

模型回答：
{answer}

只输出一行（不要任何 markdown 标记、不要加粗）：`忠实: <一句话理由>` 或 `不忠实: <一句话理由>`"""

def judge(context: str, answer: str) -> str:
    prompt = JUDGE_PROMPT.format(context=context, answer=answer)
    return chat(prompt, temperature=0.0)  # 裁判要稳定，温度 0