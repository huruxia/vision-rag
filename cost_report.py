from collections import defaultdict
from pathlib import Path

def main() -> None:
    path = Path("experiments/cost_log.tsv")
    if not path.exists():
        print("还没有成本记录——先跑一轮评测再来看")
        return
    total = 0.0
    days = defaultdict(float)
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        parts = line.split("\t")
        days[parts[0][:10]] += float(parts[-1])
        total += float(parts[-1])
    print(f"累计 LLM 花费：{total:.4f} 元")
    for day, c in sorted(days.items()):
        print(f"  {day}: {c:.4f} 元")

if __name__ == "__main__":
    main()
