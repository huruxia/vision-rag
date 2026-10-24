from .generate import answer
from .retrieve import retrieve
from .evaluate import EVAL
from .faithfulness import judge

def run() -> None:
    faithful = 0
    for item in EVAL:
        q = item["q"]
        print(f"\n问题: {q}")
        results = retrieve(q, top_k=3)
        context = "\n\n".join(r["text"] for _, r in results)
        a = answer(q)
        print(f"回答: {a}")
        verdict = judge(context, a)
        print(f"裁判: {verdict}")
        faithful += verdict.startswith("忠实")
    n = len(EVAL)
    print(f"\n忠实率: {faithful}/{n} = {faithful / n:.2f}")

if __name__ == "__main__":
    run()
