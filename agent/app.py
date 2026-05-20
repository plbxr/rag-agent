"""
Gradio Web 前端 - 提供可视化的对话界面
"""
import gradio as gr
from rag_agent import RAGAgent

agent = RAGAgent()


def chat(message, history):
    """Gradio 对话回调"""
    try:
        response = agent.chat(message)
        return response
    except Exception as e:
        return f"出错了：{e}"


def clear():
    """清空对话历史"""
    agent.clear_history()
    return []


demo = gr.ChatInterface(
    fn=chat,
    title="RAG Agent",
    description="基于 mimo + openGauss 的智能问答 Agent，支持工具调用和知识库检索",
    examples=[
        "请计算 (100+200)*3",
        "openGauss 中事务回滚的限制有哪些？",
        "什么是向量数据库？",
    ],
    cache_examples=False,
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
