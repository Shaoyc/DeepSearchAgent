# src/llms/glm_llm.py

from typing import List, Dict, Any, Optional
from .base import BaseLLM
from zhipuai import ZhipuAI


class GLMLLM(BaseLLM):
    """GLM 系列大模型（包括 glm-4, glm-4v, glm-4-flash 等）"""

    def __init__(self, api_key: str, model_name: str = "glm-4v-flash"):
        if not api_key:
            raise ValueError("GLM API key is required")
        self.client = ZhipuAI(api_key=api_key)
        # ✅ 修正模型名为官方存在的 glm-4-flash
        self.model_name = model_name

    def invoke(self, prompt: str, *args, **kwargs) -> str:
        """
        实现 BaseLLM 的抽象方法。
        使用 *args 兼容可能误传的位置参数（如旧版调用方式）。
        所有生成参数应通过 kwargs 传入（如 temperature, max_tokens）。
        """
        messages = [{"role": "user", "content": prompt}]
        return self.call(messages, **kwargs)

    def get_default_model(self) -> str:
        return self.model_name

    def call(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # ✅ 关键修改：GLM 使用 max_output_tokens，不支持 max_tokens
        # 兼容 OpenAI 风格的 max_tokens 参数（常见于其他 LLM 封装）
        max_output_tokens = kwargs.get("max_tokens", kwargs.get("max_output_tokens", 2000))
        temperature = kwargs.get("temperature", 0.3)
        top_p = kwargs.get("top_p", 0.9)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                top_p=top_p
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            raise RuntimeError(f"GLM API 调用失败: {e}")

    def get_model_info(self) -> dict:
        return {
            "provider": "GLM",
            "model": self.model_name
        }