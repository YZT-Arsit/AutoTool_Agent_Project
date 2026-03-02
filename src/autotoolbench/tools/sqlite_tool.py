from __future__ import annotations
import sqlite3
from typing import Any, Dict
import os

from .base import Tool, ToolResult

DB_PATH = os.path.abspath(os.path.join(os.getcwd(), "data/sample.db"))

class SQLiteTool(Tool):
    name: str = "sql_query"
    description: str = "Execute read-only SQL on local sample.db"
    input_schema: dict = {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}

    def run(self, inp: Dict[str, Any]) -> ToolResult:
        q = inp.get("query", "")
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(q)
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            return ToolResult(ok=True, output=rows)
        except Exception as e:
            return ToolResult(ok=False, error=str(e))


# register
from .registry import register
register(SQLiteTool())
