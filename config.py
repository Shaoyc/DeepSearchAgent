# Deep Search Agent 配置文件
# 请在这里填入您的API密钥

# DeepSeek API Key
DEEPSEEK_API_KEY = "sk-7f8dfe583fe54aa18765be6159adcda0"

# OpenAI API Key (可选)
OPENAI_API_KEY = "your_openai_api_key_here"

GLM_API_KEY = "65db00be5530420a1d1aa25a0ae33085.mzd6x3VshRAa4IFB"

# Tavily搜索API Key
TAVILY_API_KEY = "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"

# 配置参数
# DEFAULT_LLM_PROVIDER = "deepseek"
# DEEPSEEK_MODEL = "deepseek-chat"
# OPENAI_MODEL = "gpt-4o-mini"

DEFAULT_LLM_PROVIDER = "glm"
GLM_MODEL = "glm-4v-flash"

MAX_REFLECTIONS = 2
SEARCH_RESULTS_PER_QUERY = 3
SEARCH_CONTENT_MAX_LENGTH = 20000
OUTPUT_DIR = "reports"
SAVE_INTERMEDIATE_STATES = True
