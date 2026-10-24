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
- [ ] **相对导入 `from .config import` 的适用范围** —— 照抄用了，但不完全理解
  为什么不能直接运行 `llm.py`（会报 attempted relative import）

### Git 与 GitHub
- [ ] **commit message 的规范**（feat / fix / docs / chore 前缀约定）—— 照抄了，
  不懂这套约定的来源（Conventional Commits）和为什么公司都在用
- [ ] **git push 报 `fatal: 'origin' does not appear to be a git repository` 的原理** ——
  当时是执行顺序反了（先 push 后加 remote），重跑就好了，但没深究 remote 的机制

---

## W1 · Day 3（2026-10-24）

### 两个仓库与"改错文件"（★ 两次排查事故）
- [ ] **电脑上有两个 vision-rag 仓库** —— 真实开发仓库 `C:\Users\huruxia\vision-rag` 和桌面副本 `Desktop\agent\vision-rag`（旧快照），
  检查/操作认准真实仓库，副本只当快照，否则会"看着改了其实没改"
- [ ] **同名代码写在多个文件里** —— llm.py 和 chat_cli.py 都有 `model="deepseek-flash"`，
  做防崩测试时改错了文件（改了 llm.py，程序实际走 chat_cli.py）。
  教训：改前确认文件在运行链上（看 main.py import 了什么）；改完用全局搜索自检只改对了一处

### 双重 API 调用（★ 最烧钱的 bug）
- [ ] **try/except 是"插入"不是"替换"** —— 加防崩代码时旧的 `stream_chat` 调用没删，
  导致每句话被调两次 API（回答两次、花费 double）。排查法：现象（两次回答）→ 假设（两次调用）→ 读代码证实（run() 里两个 stream_chat）

### 模型与计费（Day 3 实测发现）
- [ ] **DeepSeek 缓存对小 prompt 不生效** —— 输入 37~98 token 时命中恒为 0；
  缓存需重复前缀足够长才启动，等 RAG 长上下文阶段再验证
- [ ] **DeepSeek 当前支持的模型名** —— `deepseek-flash` 和 `deepseek-v4-pro`（来自报错信息，以官网为准）
- [ ] **第二轮输入 token 反常** —— 第二轮输入 98 < 第一轮输入 37 + 第一轮输出 122，
  疑似服务端上下文压缩或统计口径问题，待长上下文阶段再查

---

## 已清偿（学懂了的，留档）
（暂无——清偿后把条目移到这里，写一句"学懂了什么"）
