# RAG Agent - 基于 mimo + openGauss 的智能问答 Agent

一个具备 **RAG 检索**、**工具调用 (Tool Use)** 和 **对话记忆** 的智能问答系统。基于小米 mimo 大模型和华为 openGauss 向量数据库构建。

## 架构

```
用户提问
   │
   ▼
┌──────────────┐
│   RAG Agent  │ ◄── 对话记忆（多轮上下文）
│  (mimo LLM)  │
└──────┬───────┘
       │ Agent 自主决策：是否调用工具？
       ▼
┌──────────────┐     ┌───────────────────┐
│  Tool Use    │────▶│   calculator      │ 数学计算
│  工具调用     │────▶│   search_knowledge│ openGauss 向量检索
└──────────────┘     └───────────────────┘
                              │
                              ▼
                     ┌───────────────────┐
                     │ openGauss + pgvector│
                     │   向量数据库        │
                     └───────────────────┘
                              │
                              ▼
                     ┌───────────────────┐
                     │  Ollama           │
                     │ nomic-embed-text  │ 文本向量化
                     └───────────────────┘
```

## 核心能力

| 能力 | 说明 |
|------|------|
| **RAG 检索** | 从 openGauss 向量数据库中检索相关知识，基于事实回答 |
| **Tool Use** | Agent 自主决定调用哪个工具，支持计算器和知识库检索 |
| **对话记忆** | 多轮对话，记住上下文 |
| **降级机制** | 知识库不可用时，自动降级到模型自身知识 |

## 技术栈

- **LLM**: 小米 mimo-v2.5-pro（OpenAI 兼容 API）
- **向量数据库**: openGauss + pgvector
- **Embedding**: Ollama + nomic-embed-text
- **Agent 框架**: OpenAI Function Calling
- **Web API**: FastAPI
- **前端**: Gradio

## 项目结构

```
agent/
├── config.py          # 配置文件（API密钥、数据库连接）
├── tools.py           # 工具定义（OpenAI Function Calling 格式）
├── rag_agent.py       # 核心 Agent（对话 + 工具调用循环）
├── api.py             # FastAPI Web 接口
├── app.py             # Gradio 可视化前端
└── requirements.txt   # Python 依赖
```

## 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt
```

需要以下服务运行：

- **openGauss** 数据库（端口 5432）
- **Ollama** 本地模型服务（端口 11434）

```bash
# 拉取 embedding 模型
ollama pull nomic-embed-text
```

### 2. 数据库初始化

使用原始的 `final.py` 初始化数据库和向量数据：

```bash
cd ..
python final.py
```

### 3. 运行

**命令行模式：**

```bash
python rag_agent.py
```

**Web API 模式：**

```bash
python api.py
# 访问 http://localhost:8000/docs 查看 API 文档
```

**Gradio 可视化模式：**

```bash
python app.py
# 访问 http://localhost:7860
```

## 对话示例

```
你: 请计算 (100+200)/3
  [调用工具] calculator({'expression': '(100+200)/3'})
  [工具结果] 100.0...
Agent: (100+200)/3 = 100

你: openGauss 中事务回滚的限制有哪些？
  [调用工具] search_knowledge({'query': 'openGauss 事务回滚 限制'})
  [工具结果] ...
Agent: 基于知识库内容，openGauss 事务回滚的主要限制包括：
1. 已提交的事务无法回滚
2. DDL 语句自动提交...
```

## 配置说明

在 `config.py` 中修改：

| 配置项 | 说明 |
|--------|------|
| `API_KEY` | mimo API 密钥 |
| `API_BASE_URL` | API 地址 |
| `MODEL_NAME` | 模型名称 |
| `DB_CONFIG` | openGauss 数据库连接信息 |
| `OLLAMA_HOST` | Ollama 服务地址 |

## 扩展方向

- 添加更多工具（网络搜索、数据库查询、文件操作等）
- 支持多模型切换（Claude、GPT-4、DeepSeek 等）
- 添加用户认证和会话管理
- 部署到云端（Docker 容器化）
