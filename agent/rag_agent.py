"""
RAG Agent - 基于mimo API的智能问答Agent
核心能力：RAG检索 + 工具调用 + 对话记忆
"""
from openai import OpenAI
import json
from tools import TOOLS, TOOL_DISPATCH
from config import API_KEY, API_BASE_URL, MODEL_NAME

SYSTEM_PROMPT = """你是一个基于openGauss知识库的智能助手。

你的能力：
1. 使用search_knowledge工具从openGauss知识库检索相关信息来回答问题
2. 使用calculator工具进行数学计算
3. 记住对话上下文，进行多轮对话

回答规则：
- 优先使用检索到的知识库内容回答
- 如果知识库没有相关信息，基于你的知识回答并说明来源
- 回答要简洁、准确、分点清晰"""


class RAGAgent:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
        self.history = []

    def chat(self, user_message: str) -> str:
        """与Agent对话，自动处理工具调用循环"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self.history,
            {"role": "user", "content": user_message}
        ]

        # Agent循环：持续调用直到得到最终回复
        while True:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                max_tokens=4096,
                tools=TOOLS,
                messages=messages
            )

            msg = response.choices[0].message

            # 如果没有工具调用，返回最终回复
            if not msg.tool_calls:
                self.history.append({"role": "user", "content": user_message})
                self.history.append({"role": "assistant", "content": msg.content})
                return msg.content

            # 有工具调用：执行工具并将结果返回
            messages.append(msg)

            for call in msg.tool_calls:
                func_name = call.function.name
                func_args = json.loads(call.function.arguments)
                print(f"  [调用工具] {func_name}({func_args})")

                result = TOOL_DISPATCH[func_name](func_args)
                print(f"  [工具结果] {result[:100]}...")

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                })

    def clear_history(self):
        """清空对话历史"""
        self.history = []


def main():
    """交互式对话入口"""
    print("=" * 60)
    print("  RAG Agent - 基于mimo + openGauss的智能问答")
    print("  输入 'quit' 退出 | 'clear' 清空对话历史")
    print("=" * 60)

    agent = RAGAgent()

    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("再见！")
            break
        if user_input.lower() == "clear":
            agent.clear_history()
            print("对话历史已清空")
            continue

        try:
            response = agent.chat(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"\n错误: {e}")


if __name__ == "__main__":
    main()
