from __future__ import annotations
import os
import re
from typing import Any, Dict, List

from .base import Tool, ToolResult
from .registry import register

LOG_PATH = os.path.abspath(os.path.join(os.getcwd(), "data/logs/app.log"))

class LogSearchTool(Tool):
    name: str = "log_search"
    description: str = "Search app.log for keyword or regex"
    input_schema: dict = {"type":"object","properties":{"pattern":{"type":"string"}},"required":["pattern"]}

    def run(self, inp: Dict[str, Any]) -> ToolResult:
        pat = inp.get("pattern","")
        try:
            with open(LOG_PATH) as f:
                lines = f.readlines()
            res: List[str] = []
            try:
                regex = re.compile(pat)
                for l in lines:
                    if regex.search(l):
                        res.append(l.strip())
            except re.error:
                # treat as substring
                for l in lines:
                    if pat in l:
                        res.append(l.strip())
            return ToolResult(ok=True, output=res)
        except Exception as e:
            return ToolResult(ok=False, error=str(e))

register(LogSearchTool())
