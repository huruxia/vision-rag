# 评测体系手册（W2 收官版 · 2026-10-25）

## 三把尺子
| 评测 | 命令 | 量什么 | 当前基线 |
|---|---|---|---|
| 检索质量 | `uv run python -m vision_rag.evaluate` | 有答案卷 Recall@1/@3、MRR；无答案卷 top1 分数（拒答边界） | R@1=1.00、R@3=1.00、MRR=1.00；阈值 0.45 |
| 生成忠实度 | `uv run python -m vision_rag.eval_faithfulness` | 回答忠于资料的比例（LLM 裁判，需人工抽查） | 10/10 |
| 精排质量 | `uv run python demo_rerank.py` | 粗排 vs 精排 top3 对比（人工判断合理性） | 粗排 10/10、精排 10/10 |

## 何时跑（回归守则）
- 改检索（embed / index / retrieve / bm25 / hybrid）→ 跑 evaluate + demo_rerank
- 改生成（generate / llm / prompt）→ 跑 eval_faithfulness
- 改文档 / 重建索引 → 先 `uv run python -m vision_rag.index` 再全跑
- 任何升级 → 三件套全跑，防止"排序分当置信度"这类回归（W2D5 教训）

## 当前链路
问题 → 混合检索(BM25+向量+RRF) → Rerank(LLM 精排) → 阈值闸门(0.45) → 生成 → 忠实度兜底

## 已知边界
- 0.45 阈值与 1.00 分数是"4+2 篇玩具文档"红利，真实数据需重标
- LLM 裁判/法官会误判（W2D4/W2D6 实证），评测结论必须人工抽查
- 数据变 → 基线变：每次改文档后重新记录基线
