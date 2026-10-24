# VisionRAG

多模态图文检索问答系统（视觉 × Agent 交叉方向练手项目）。

## 这是什么

企业内部积累了海量图文混排文档（技术手册、论文、器件资料），传统关键词检索找不到图，纯文本 RAG 又丢失图像信息。本项目构建同时索引图像与文本的 RAG 系统，支持以文搜图和图文混合问答，每个答案都能溯源到具体图片与段落。

**当前状态**：v0 文本 RAG 已端到端跑通（检索 → 拼提示词 → 生成，含拒答）。

## 快速开始（5 分钟）

```bash
# 1. 环境要求：Python 3.10+，已安装 uv
uv sync

# 2. 配置密钥：复制模板为 .env 并填入两个 key
copy .env.example .env

# 3. 建索引（把内置 4 篇文档切块嵌入 → data/index/v0.json）
uv run python -m vision_rag.index

# 4. 跑起来
uv run python main.py
```

预期效果：

```text
问题: 什么是RAG
RAG（检索增强生成）是一种让大模型基于资料回答问题的技术……
问题: 今天上海天气怎么样
不知道。资料中没有上海天气的信息。
```

## 项目结构

```
vision-rag/
├── src/vision_rag/        # 核心代码
│   ├── config.py          # 读取 .env 配置
│   ├── llm.py             # DeepSeek 生成（支持温度参数）
│   ├── chat_cli.py        # 流式聊天工具（开发用，含 !temp 命令）
│   ├── cost.py            # API 费用计算
│   ├── embed.py           # 通义 text-embedding-v3 嵌入
│   ├── index.py           # 分块 + 建索引 → data/index/v0.json
│   ├── retrieve.py        # 余弦相似度检索 top-k
│   └── generate.py        # 检索结果拼提示词 → 答案（RAG 主链路）
├── data/                  # 数据（gitignored）
├── experiments/           # 实验记录
├── main.py                # 主入口：RAG 问答
├── demo_retrieve.py       # 检索演示工具
├── DEBT.md                # 欠债清单（踩坑记录，面试素材）
└── pyproject.toml
```

## 当前进度

- [x] v0：文本 RAG 端到端跑通（检索 + 生成 + 拒答）
- [x] 成本计费 + 温度控制
- [ ] v1：检索质量优化（混合检索 + Rerank + 评测）
- [ ] v2：多模态支持（图像索引 + VLM 问答）
- [ ] v3：服务化上线（FastAPI + Docker + 追踪）

## 技术栈

Python · uv · DeepSeek(deepseek-flash) · 通义(text-embedding-v3) · openai SDK
（规划：FastAPI · pgvector · Langfuse · RAGAS）

## 成本估算

按 deepseek-flash 空闲时段定价（输入 1 元 / 输出 4 元，每百万 token）：

- 单次问答 ≈ 输入 300 + 输出 400 token ≈ 0.0003 + 0.0016 ≈ **0.002 元**
- 50 元预算 ≈ 25,000 次调用

## 相关文档

- [DEBT.md](DEBT.md)：欠债清单（每周更新，面试素材）
- experiments/：实验记录（如 temperature_20261024.md）
- 掘金博客：W1 复盘《从零搭出能回答"自己文档"的 RAG：179 行代码，成本不到 1 毛》<https://juejin.cn/post/7699732988154544143>
