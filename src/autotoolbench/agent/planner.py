from __future__ import annotations
from typing import Any, Dict, List

class Planner:
    def __init__(self, llm):
        self.llm = llm

    def plan(self, instruction: str) -> List[Dict[str, Any]]:
        # naive: split on periods into steps
        steps: list[Dict[str, Any]] = []
        # split on ' and ' to get multiple actions
        parts = [p.strip() for p in instruction.replace(',', ' ').split(' and ')]
        for i, part in enumerate(parts):
            if not part:
                continue
            tool = "noop"
            args: Dict[str, Any] = {}
            lower = part.lower()
            if "select" in lower:
                tool = "sql_query"
                # simple query extraction
                args["query"] = part
            elif "write" in lower or "save" in lower:
                tool = "file_write"
                # try to extract filename
                import re
                m = re.search(r"(?:to|save) (?:file )?([\w\.]+)", lower)
                if m:
                    args["path"] = m.group(1)
                args.setdefault("content", "")
            elif "read" in lower:
                tool = "file_read"
                m = re.search(r"read (?:file )?([\w\.]+)", lower)
                if m:
                    args["path"] = m.group(1)
            elif "log" in lower:
                tool = "log_search"
                # pattern
                args["pattern"] = "ERROR" if "error" in lower else ""
            # apply noise
            if hasattr(self.llm, "maybe_corrupt"):
                args = self.llm.maybe_corrupt({"args": args}).get("args", args)
            steps.append({"step": i+1, "subgoal": part, "tool": tool, "args": args})
        return steps
