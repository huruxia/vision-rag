import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from vision_rag.hybrid import search
from vision_rag.rerank import rerank
from vision_rag.evaluate import EVAL

def main() -> None:
    for item in EVAL:
        q = item["q"]
        coarse = search(q, top_k=6)        # 粗排捞 6 个候选
        fine = rerank(q, coarse)           # 精排只挑 top3 用
        c_ids = [r["doc_id"] for _, r in coarse]
        f_ids = [r["doc_id"] for _, r in fine[:3]]
        print(f"[{q[:12]:<12}] 粗排={c_ids}\n{'':<24}精排={f_ids}")

if __name__ == "__main__":
    main()
