from __future__ import annotations
from typing import List, Dict

class LLMBase:
    def generate(self, messages: List[Dict]) -> str:
        """Generate a response based on a list of messages.
        Each message is a dict with 'role' and 'content'.
        """
        raise NotImplementedError
