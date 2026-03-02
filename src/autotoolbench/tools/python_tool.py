from __future__ import annotations
import sys
import time
import threading
from typing import Any, Dict

from .base import Tool, ToolResult
from .registry import register

SAFE_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'print': print,
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'dict': dict,
    'list': list,
    'set': set,
}

class PythonExecTool(Tool):
    name: str = "python_exec"
    description: str = "Execute simple Python code in sandbox"
    input_schema: dict = {"type":"object","properties":{"code":{"type":"string"}},"required":["code"]}

    def run(self, inp: Dict[str, Any]) -> ToolResult:
        code = inp.get("code","")
        output = {}
        # restricted exec environment
        loc = {}
        glb = {"__builtins__": SAFE_BUILTINS}
        try:
            exec(code, glb, loc)
            return ToolResult(ok=True, output=loc)
        except Exception as e:
            return ToolResult(ok=False, error=str(e))

register(PythonExecTool())
