from .llm import chat

RERANK_PROMPT = """你是检索精排法官。给定问题和候选片段列表，把候选按与问题的相关性从高到低排序。
注意：如果多个候选都与问题相关，优先选择"直接、完整回答该问题"的候选，把只沾边的候选排后面。

问题：{question}

候选：
{numbered}

只输出候选编号序列（逗号分隔，不要任何其他文字或标点）：例如 3,1,4,2"""

def rerank(question: str, results: list[tuple[float, dict]]) -> list[tuple[float, dict]]:
    numbered = "\n".join(
        f"[{i}] {item['text']}" for i, (_, item) in enumerate(results)   # 全文，不截断
    )

    resp = chat(RERANK_PROMPT.format(question=question, numbered=numbered), temperature=0.0)
    order = [int(x) for x in resp.replace("，", ",").split(",") if x.strip().isdigit()]
    order = [i for i in order if 0 <= i < len(results)]        # 越界编号丢弃（容错）
    rest = [r for j, r in enumerate(results) if j not in order]  # 漏排的补在末尾
    return [results[i] for i in order] + rest
