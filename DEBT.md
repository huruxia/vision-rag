# 欠债清单（DEBT.md）

> 用法：遇到不懂但暂时绕过的问题，记一行。S2 阶段（W4–W6）集中清偿。
> 格式：- [ ] 问题描述 —— 当时怎么绕过的

---

## W1 · Day 1（2026-10-22）

- [ ] **conda 的 base 环境是什么** —— 当时不明白 `(base)` 前缀含义，只照抄执行了 `conda config --set auto_activate_base false` 关掉了。需要补：虚拟环境的意义、conda 和 uv 的关系
- [ ] **GitHub 网页打不开的网络原理** —— 当时只换了时间/网络就通了，不懂为什么国内访问不稳定，代理原理没搞懂

## W1 · Day 2（2026-10-23）

### 零宽空格事件（★ 最重要的教训，两次踩坑）
- [ ] **零宽空格（U+200B）是什么** —— 从网页/聊天窗口复制代码时带入了不可见字符，
  导致 `if __name__ == "__main__":` 永远为 False。踩了两次：greet.py 和 main.py。
  排查方法：`len('__main__')` 应为 8，多 1 就是有脏字符。
- [ ] **三条防御规矩**：① 复制代码后先跑最小打印验证；② 「看起来对但行为不对」
  第一反应查不可见字符；③ 关键行手敲不复制

### PowerShell vs Python 解释器
- [ ] **终端和 REPL 的区别** —— 曾把 `>>> import fibo` 敲进 PowerShell 报错。
  `PS>` 开头 = 操作系统命令；`>>>` = 已进入 Python 解释器才能敲 Python 代码

### uv 与包管理
- [ ] **uv sync 的静态快照机制** —— 新增 .py 文件后包没刷新，报
  `ModuleNotFoundError: No module named 'vision_rag.llm'`。
  原因：uv 把项目包装进虚拟环境时记录的是文件清单快照，新增文件不在里面。
  解法：`uv sync --reinstall-package vision-rag` 或 main.py 里手动 `sys.path.insert`
- [ ] **pyproject.toml 里的 `[tool.hatch.build.targets.wheel]` 配置** ——
  照抄了 `dev-mode-dirs = ["src"]`，不懂 editable 安装 / 静态复制的区别
- [ ] **为什么要用 openai 这个包调 DeepSeek** —— 因为 OpenAI 兼容 API 是行业事实标准，
  但没深入理解"兼容层"的概念

### Python 语法与工程
- [ ] **`__init__.py` 的完整用法** —— 做了 mypkg 实验理解了"前台接待"作用，
  但还没在实际项目里用过（vision_rag 的 `__init__.py` 还是空的）
- [ ] **中文路径风险** —— 练习目录用了 `D:\python模块学习示例`，被提醒改英文路径，
  但不知道具体哪些工具链会因中文路径出错
- [ ] **相对导入 `from .config import` 的适用范围** —— 照抄用了，但不完全理解
  为什么不能直接运行 `llm.py`（会报 attempted relative import）

### Git 与 GitHub
- [ ] **commit message 的规范**（feat / fix / docs / chore 前缀约定）—— 照抄了，
  不懂这套约定的来源（Conventional Commits）和为什么公司都在用
- [ ] **git push 报 `fatal: 'origin' does not appear to be a git repository` 的原理** ——
  当时是执行顺序反了（先 push 后加 remote），重跑就好了，但没深究 remote 的机制

---

## 已清偿（学懂了的，留档）
（暂无——清偿后把条目移到这里，写一句"学懂了什么"）
