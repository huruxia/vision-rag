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
    hit = getattr(usage, "prompt_cache_hit_tokens", 0)
    miss = getattr(usage, "prompt_cache_miss_tokens", 0)
    if hit + miss == 0:                      # 老接口没有缓存字段时，退回全未命中
        miss = usage.prompt_tokens
    cost = (
        hit / 1_000_000 * p["input_hit"]
        + miss / 1_000_000 * p["input_miss"]
        + usage.completion_tokens / 1_000_000 * p["output"]
    )
    return cost

