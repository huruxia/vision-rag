from openai import OpenAI
from .config import get_api_key

client = OpenAI(
    api_key=get_api_key("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def embed(text: str) -> list[float]:
    resp = client.embeddings.create(
        model="text-embedding-v3",
        input=[text],
    )
    return resp.data[0].embedding
