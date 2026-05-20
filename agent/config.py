"""
配置文件 - API密钥和数据库连接信息
"""
import os

# ===================== API 配置 =====================
API_KEY = os.getenv("API_KEY", "tp-cgjgbsxzfbxc9l3s1nh1ijwqr39hk4wcgp01i8jo77cbujvd")
API_BASE_URL = os.getenv("API_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
MODEL_NAME = "mimo-v2.5-pro"

# ===================== openGauss 数据库配置 =====================
DB_CONFIG = {
    "database": "postgres",
    "user": "rag_user",
    "password": "Rag@12345",
    "host": "127.0.0.1",
    "port": "5432"
}
TABLE_NAME = "analyze_rag_table"

# ===================== Ollama 本地模型配置（用于embedding） =====================
OLLAMA_HOST = "http://127.0.0.1:11434"
EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_DIM = 768
