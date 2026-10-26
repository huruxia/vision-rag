from datetime import datetime
from pathlib import Path

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

def log_usage(usage, model: str = "deepseek-flash") -> float:
    """把一次调用的用量和花费追加到 experiments/cost_log.tsv，返回花费（元）"""
    cost = calc_cost(usage, model)
    Path("experiments").mkdir(exist_ok=True)
    hit = getattr(usage, "prompt_cache_hit_tokens", 0)
    miss = getattr(usage, "prompt_cache_miss_tokens", 0)
    if hit + miss == 0:
        miss = usage.prompt_tokens
    line = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\t"
        f"{usage.prompt_tokens}\t{hit}\t{miss}\t{usage.completion_tokens}\t{cost:.6f}\n"
    )
    with open("experiments/cost_log.tsv", "a", encoding="utf-8") as f:
        f.write(line)
    return cost


