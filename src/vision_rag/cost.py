# 价格单位：元 / 每百万 token
# 来源：api-docs.deepseek.com/quick_start/pricing（2026-10-23 查）
PRICE = {
    "deepseek-flash": {
        "input_hit": 0.02,      # 缓存命中（空闲）
        "input_miss": 1.0,      # 缓存未命中（空闲）
        "output": 4.0,          # 输出（空闲）
    },
}

def calc_cost(usage, model: str = "deepseek-flash") -> float:
    p = PRICE[model]
    # 简化版：假设全部未命中（保守估算）
    cost = (
        usage.prompt_tokens / 1_000_000 * p["input_miss"]
        + usage.completion_tokens / 1_000_000 * p["output"]
    )
    return cost
