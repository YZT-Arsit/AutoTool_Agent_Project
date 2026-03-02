from __future__ import annotations
from typing import Dict

class Reflector:
    def classify(self, traj_step: Dict) -> str:
        # naive rule based
        if traj_step.get("error"):
            return "BAD_TOOL_ARGS"
        return "PLAN_ERROR"

    def suggest_fix(self, issue: str) -> str:
        return f"Please fix {issue}"
