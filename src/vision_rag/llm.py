from openai import OpenAI
from .config import get_api_key
from .cost import log_usage

client = OpenAI(
    api_key=get_api_key("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

def chat(prompt: str, temperature: float = 1.0) -> str:
    resp = client.chat.completions.create(
        model="deepseek-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    log_usage(resp.usage)                      # ← 埋点：每次调用自动记账
    return resp.choices[0].message.content
