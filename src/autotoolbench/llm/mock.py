from __future__ import annotations
import random
import json
from typing import List, Dict, Optional
from .base import LLMBase

class MockLLM(LLMBase):
    def __init__(self, seed: Optional[int] = None, noise: float = 0.0):
        self.random = random.Random(seed)
        self.noise = noise

    def generate(self, messages: List[Dict]) -> str:
        # simple template-based response: look for keywords in last message
        last = messages[-1]["content"]
        # if asking for plan, return JSON list
        if "plan" in last.lower():
            plan = [
                {"step": i+1, "action": "tool", "tool": "noop", "args": {}} 
                for i in range(2)
            ]
            return json.dumps(plan)
        # if asking for tool call, return simple structure
        if "tool" in last.lower():
            # random tool name as placeholder
            return json.dumps({"tool": "noop", "args": {}})
        # default: echo
        res = f"MOCK_RESPONSE: {last}"
        return res

    def maybe_corrupt(self, data: Dict) -> Dict:
        if self.noise > 0 and self.random.random() < self.noise:
            # randomly corrupt one value to none
            if data.get("args"):
                data["args"] = {}
        return data
