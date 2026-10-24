from openai import OpenAI
from .config import get_api_key
from .cost import calc_cost


client = OpenAI(
    api_key=get_api_key("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def stream_chat(messages: list[dict],temperature:float = 0.9) -> str:
    resp = client.chat.completions.create(
        model="deepseek-flash",                   
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},    # ← 关键：流式也返回用量
        temperature=temperature,
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
        print(f"[本次用量] 输入 {usage.prompt_tokens}(命中{usage.prompt_cache_hit_tokens}/未命中{usage.prompt_cache_miss_tokens}),输出 {usage.completion_tokens}")
        print(f"[本次花费] 约 {calc_cost(usage):.6f} 元")
    return full



def run():
    messages = [{"role": "system", "content": "你是一个简洁的助手"}]
    temperature = 0.9
    while True:
        user = input("\n你: ")
        if user.lower() in ("exit", "quit"):
            break
        if user.startswith("!temp"):
            parts = user.split()
            if len(parts) == 1:
                print(f"[当前温度 {temperature}]")
                continue
            temperature = float(parts[1])
            print(f"[温度已设为 {temperature}]")
            continue
        messages.append({"role": "user", "content": user})
        try:
            answer = stream_chat(messages,temperature=temperature)
        except Exception as e:
            print(f"[出错了] {e} —— 请检查网络或余额")
            messages.pop()
            continue
        messages.append({"role": "assistant", "content": answer})
