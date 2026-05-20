"""
工具定义 - Agent可以调用的外部工具
"""
import psycopg2
import ollama
from config import DB_CONFIG, TABLE_NAME, OLLAMA_HOST, EMBEDDING_MODEL

# ===================== 工具实现 =====================

def calculator(expression: str) -> str:
    """安全计算数学表达式"""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "错误：只支持数字和 +-*/.() 运算符"
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"计算错误：{e}"


def search_knowledge(query: str) -> str:
    """从openGauss向量数据库中检索相关知识"""
    try:
        client = ollama.Client(host=OLLAMA_HOST)
        emb = client.embeddings(model=EMBEDDING_MODEL, prompt=query)["embedding"]
        emb_str = "[" + ",".join(map(str, emb)) + "]"

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(f"""
            SELECT content FROM {TABLE_NAME}
            ORDER BY emb <-> vector('{emb_str}')
            LIMIT 3
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return "未找到相关信息"
        return "\n---\n".join(row[0] for row in rows)
    except Exception as e:
        return f"检索失败：{e}"


# ===================== OpenAI 格式工具定义 =====================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持加减乘除和括号。例如：2+3*4, (10-2)/2",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，如 '2+3*4'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "从openGauss知识库中检索相关信息。当用户询问openGauss相关问题时使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用于检索的查询文本"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# 工具分发表
TOOL_DISPATCH = {
    "calculator": lambda args: calculator(args["expression"]),
    "search_knowledge": lambda args: search_knowledge(args["query"]),
}
