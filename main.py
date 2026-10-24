import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from vision_rag.generate import answer

def main():
    while True:
        q = input("\n问题: ")
        if q.lower() in ("exit", "quit"):
            break
        print(answer(q))

if __name__ == "__main__":
    main()
