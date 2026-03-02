from __future__ import annotations
from typing import Dict

class BudgetController:
    def __init__(self, max_calls=10, max_steps=10, max_time=60, max_tokens=1000):
        self.max_calls = max_calls
        self.max_steps = max_steps
        self.max_time = max_time
        self.max_tokens = max_tokens

    def initial(self) -> Dict[str, Any]:
        return {"calls":0,"steps":0,"time":0.0,"tokens":0}

    def check(self, budget: Dict[str, Any]) -> bool:
        return (budget.get("calls",0) < self.max_calls and
                budget.get("steps",0) < self.max_steps)
