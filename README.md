# VisionRAG

多模态图文检索问答系统（视觉 × Agent 交叉方向练手项目）

## 这是什么
企业内部积累了大量图文混排文档（技术手册、论文、器件资料），
传统关键词检索找不到图，纯文本 RAG 又丢失图像信息。
本项目构建同时索引图像与文本的 RAG 系统，
支持以文搜图和图文混合问答，每个答案都能溯源到具体图片与段落。

## 快速开始

```bash
# 安装依赖
uv sync

# 配置密钥（复制 .env.example 为 .env 并填入）
# DEEPSEEK_API_KEY=...
# DASHSCOPE_API_KEY=...

# 运行
uv run python main.py
```

## 当前进度
- [x] v0：文本 RAG 端到端跑通（进行中）
- [ ] v1：检索质量优化（混合检索 + Rerank + 评测）
- [ ] v2：多模态支持（图像索引 + VLM 问答）
- [ ] v3：服务化上线（FastAPI + Docker + 追踪）

## 技术栈
Python · uv · FastAPI · pgvector · DeepSeek · 通义千问 · Langfuse · RAGAS

## 本周踩过的坑
（每周五更新，面试素材）

## 成本估算

输入 300 token + 输出 400 token
单次成本（空闲，未命中缓存）= 300/1M × 1 + 400/1M × 4
                          = 0.0003 + 0.0016
                          ≈ 0.002 元（2 厘钱）

50 元 ÷ 0.002 元/次 ≈ 25,000 次

按 deepseek-flash 空闲时段定价，单次问答约 0.002 元。
50 元预算可支撑约 25,000 次调用。
