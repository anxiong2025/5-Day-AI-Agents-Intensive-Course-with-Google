# 5-Day AI Agents Intensive Course with Google

> **42万+开发者参与的 AI Agent 课程** | 感谢 [sdivyanshu90](https://github.com/sdivyanshu90/5-Day-AI-Agents-Intensive-Course-with-Google) 和 Google 提供的免费课程资源

5 天直播回放视频：[youtube](https://www.youtube.com/playlist?list=PLqFaTIg4myu9r7uRoNfbJhHUbLp-1t1YE)

## 快速开始

### 前置要求
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) 包管理工具
- Google API Key ([获取地址](https://aistudio.google.com/apikey))

### 安装配置
```bash
# 安装依赖
uv sync

# 配置 API 密钥
cp .env.example .env
# 编辑 .env 文件，添加你的 GOOGLE_API_KEY
```

### VS Code 配置
**必需插件**: Jupyter
- 安装：`Cmd+Shift+P` → "Extensions: Install Extensions" → 搜索 "Jupyter"
- 选择内核：点击笔记本中的内核选择器 → 选择 `.venv (Python 3.12.x)`

### 运行笔记本
在 VS Code 中打开 `day1/*.ipynb`，按 `Shift+Enter` 运行单元格

---

## 课程大纲与每日作业

### ✅ Day 1: Agent 入门
**主题**: Agent 分类、Agent Ops、互操作性与安全基础

- 📄 [白皮书: Introduction to Agents](https://www.kaggle.com/whitepaper-agents)
- 🎙️ [播客: Unit 1 Summary](https://www.kaggle.com/whitepaper-agents-podcast)
- 💻 **代码实验**:
  - [使用 Gemini 和 ADK 构建第一个 Agent](https://www.kaggle.com/code/markishere/day-1-prompting-with-gemini)
  - [构建第一个多 Agent 系统](https://www.kaggle.com/code/markishere/day-1-agent-architectures)
- 📚 [代码实验故障排除指南](https://www.kaggle.com/discussions/general/552193)

**本地笔记本**:
- `day1/day1-01-from-prompt-to-action.ipynb` - 基础 Agent + Google 搜索
- `day1/day1-02-agent-architectures.ipynb` - 多 Agent 模式（顺序/并行/动态）
- `day1/day1-01-First-Agent-Web-UI.py` - FastAPI Web 界面（运行: `uv run day1/day1-01-First-Agent-Web-UI.py`）

---

### Day 2: Agent 工具与互操作性 (MCP)
**主题**: 外部工具、实时数据检索、模型上下文协议 (MCP)

- 📄 [白皮书: Agent Tools & Interoperability with MCP](https://www.kaggle.com/whitepaper-agents-tools)
- 🎙️ [播客: Unit 2 Summary](https://www.kaggle.com/whitepaper-agents-tools-podcast)
- 💻 **代码实验**:
  - [使用新工具扩展 Agent 能力](https://www.kaggle.com/code/markishere/day-2-tools)
  - [工具最佳实践：MCP 与长时运行操作](https://www.kaggle.com/code/markishere/day-2-mcp-and-long-running-tools)

---

### Day 3: 上下文工程：会话与记忆
**主题**: 上下文窗口管理、会话（即时历史）、记忆（长期持久化）

- 📄 [白皮书: Context Engineering: Sessions & Memory](https://www.kaggle.com/whitepaper-agents-memory)
- 🎙️ [播客: Unit 3 Summary](https://www.kaggle.com/whitepaper-agents-memory-podcast)
- 💻 **代码实验**:
  - [实现会话管理即时上下文](https://www.kaggle.com/code/markishere/day-3-sessions)
  - [实现记忆系统实现长期个性化](https://www.kaggle.com/code/markishere/day-3-memory)

---

### Day 4: Agent 质量保障
**主题**: 评估框架、可观测性（日志/追踪/指标）、LLM-as-a-Judge、人工介入 (HITL)

- 📄 [白皮书: Agent Quality](https://www.kaggle.com/whitepaper-agents-quality)
- 🎙️ [播客: Unit 4 Summary](https://www.kaggle.com/whitepaper-agents-quality-podcast)
- 💻 **代码实验**:
  - [实现可观测性用于调试](https://www.kaggle.com/code/markishere/day-4-observability)
  - [评估你的 Agent](https://www.kaggle.com/code/markishere/day-4-evaluation)

---

### Day 5: 从原型到生产
**主题**: 部署、扩展、Agent2Agent (A2A) 协议、Vertex AI Agent Engine

- 📄 [白皮书: Prototype to Production](https://www.kaggle.com/whitepaper-agents-production)
- 🎙️ [播客: Unit 5 Summary](https://www.kaggle.com/whitepaper-agents-production-podcast)
- 💻 **代码实验**:
  - [使用 A2A 协议实现多 Agent 通信](https://www.kaggle.com/code/markishere/day-5-a2a)
  - [[可选] 部署到 Google Cloud Agent Engine](https://www.kaggle.com/code/markishere/day-5-agent-engine)

---

## 注意事项
- Kaggle 代码实验需要手机验证
- 项目使用 `.env` 存储 API 密钥（切勿将 `.env` 提交到 git）

