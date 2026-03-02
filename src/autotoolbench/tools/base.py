from __future__ import annotations
from typing import Any, Dict
from pydantic import BaseModel

class ToolResult(BaseModel):
    ok: bool
    output: Any = None
    error: str | None = None
    metadata: Dict[str, Any] = {}

class Tool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]

    def estimate_cost(self, inp: Dict[str, Any]) -> Dict[str, float]:
        return {"time": 1.0, "tokens": 1.0, "calls": 1}

    def run(self, inp: Dict[str, Any]) -> ToolResult:
        raise NotImplementedError
