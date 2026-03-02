from __future__ import annotations
from typing import Any, Dict
from .base import Tool, ToolResult
from .registry import register

class NoopTool(Tool):
    name: str = "noop"
    description: str = "No operation tool used as default"
    input_schema: dict = {"type":"object"}

    def run(self, inp: Dict[str, Any]) -> ToolResult:
        return ToolResult(ok=True, output="noop")

register(NoopTool())
