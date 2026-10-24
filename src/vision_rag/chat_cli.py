from openai import OpenAI
from .config import get_api_key
from .cost import calc_cost


client = OpenAI(
    api_key=get_api_key("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def stream_chat(messages: list[dict]) -> str:
    resp = client.chat.completions.create(
        model="deepseek-flash",                   
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},    # ← 关键：流式也返回用量
        temperature=0.9,
    )
    full = ""
    usage = None
    for chunk in resp:
        if chunk.choices and chunk.choices[0].delta.content:
            delta = chunk.choices[0].delta.content
            print(delta, end="", flush=True)
            full += delta
        if chunk.usage:                            # ← 最后一个 chunk 带 usage
            usage = chunk.usage
    print()
    if usage:
        print(f"[本次用量] 输入 {usage.prompt_tokens}，输出 {usage.completion_tokens}")
        print(f"[本次花费] 约 {calc_cost(usage):.6f} 元")
    return full



def run():
    messages = [{"role": "system", "content": "你是一个简洁的助手"}]
    while True:
        user = input("\n你: ")
        if user.lower() in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": user})
        answer = stream_chat(messages)
        messages.append({"role": "assistant", "content": answer})
