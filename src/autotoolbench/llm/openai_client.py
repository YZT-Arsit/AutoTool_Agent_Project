from __future__ import annotations
from .base import LLMBase

class OpenAIClient(LLMBase):
    def __init__(self, api_key: str):
        self.api_key = api_key
        # placeholder

    def generate(self, messages):
        raise RuntimeError("OpenAIClient not enabled by default")
