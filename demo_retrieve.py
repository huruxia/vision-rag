from vision_rag.retrieve import retrieve

while True:
    q = input("\n问题: ")
    if q.lower() in ("exit", "quit"):
        break
    for score, item in retrieve(q, top_k=3):
        print(f"[{score:.3f}] {item['text'][:35]}...")
