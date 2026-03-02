from __future__ import annotations
import os
from typing import Any, Dict

from .base import Tool, ToolResult
from .registry import register

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "data"))

class FileTool(Tool):
    name: str = "file_read"
    description: str = "Read file under data directory"
    input_schema: dict = {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}

    def run(self, inp: Dict[str, Any]) -> ToolResult:
        p = inp.get("path")
        if not isinstance(p, str):
            return ToolResult(ok=False, error="invalid path")
        # avoid directory traversal
        target = os.path.abspath(os.path.join(BASE_DIR, p))
        if not target.startswith(BASE_DIR):
            return ToolResult(ok=False, error="Path escape")
        if not os.path.isfile(target):
            return ToolResult(ok=False, error="Not found")
        try:
            with open(target, "r") as f:
                data = f.read()
            return ToolResult(ok=True, output=data)
        except Exception as e:
            return ToolResult(ok=False, error=str(e))

class FileWriteTool(FileTool):
    name: str = "file_write"
    description: str = "Write file under data directory"
    input_schema: dict = {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path","content"]}

    def run(self, inp: Dict[str, Any]) -> ToolResult:
        p = inp.get("path")
        if not isinstance(p, str):
            return ToolResult(ok=False, error="invalid path")
        target = os.path.abspath(os.path.join(BASE_DIR, p))
        if not target.startswith(BASE_DIR):
            return ToolResult(ok=False, error="Path escape")
        try:
            with open(target, "w") as f:
                f.write(inp.get("content",""))
            return ToolResult(ok=True, output="written")
        except Exception as e:
            return ToolResult(ok=False, error=str(e))

register(FileTool())
register(FileWriteTool())
