from __future__ import annotations
import subprocess
from typing import Any, Dict

from .base import Tool, ToolResult
from .registry import register

class TestTool(Tool):
    name: str = "run_tests"
    description: str = "Run pytest in workspace"
    input_schema: dict = {"type":"object","properties":{},"additionalProperties":False}

    def run(self, inp: Dict[str, Any]) -> ToolResult:
        try:
            res = subprocess.run(["pytest","-q"], capture_output=True, text=True)
            ok = res.returncode == 0
            output = res.stdout + res.stderr
            return ToolResult(ok=ok, output=output)
        except Exception as e:
            return ToolResult(ok=False, error=str(e))

register(TestTool())
