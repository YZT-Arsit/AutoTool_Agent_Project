from __future__ import annotations
from typing import Dict, Any
import random

from .schema import Trajectory
from ..env.tasks import Task
from ..tools.registry import get


class ReactAgent:
    def __init__(self, llm, max_steps=10):
        self.llm = llm
        self.max_steps = max_steps

    def run(self, task: Task, seed: int = 0, noise: float = 0.0) -> Trajectory:
        traj = Trajectory(task_id=task.task_id)
        random.seed(seed)
        for i in range(self.max_steps):
            # heuristic tool call based on instruction
            lower = task.instruction.lower()
            if "select" in lower:
                tool = get("sql_query")
                inp = {"query": task.instruction}
            elif "write" in lower or "save" in lower:
                tool = get("file_write")
                # extract filename
                import re
                m = re.search(r"(?:to|save) (?:file )?([\w\.]+)", lower)
                fname = m.group(1) if m else "output.txt"
                inp = {"path": fname, "content": ""}
            elif "log" in lower:
                tool = get("log_search")
                inp = {"pattern": "ERROR"}
            else:
                names = get_all()
                if names:
                    tool = random.choice(list(names.values()))
                else:
                    break
                inp = {}
            # noise
            if hasattr(self.llm, "maybe_corrupt"):
                inp = self.llm.maybe_corrupt({"args": inp}).get("args", inp)
            res = tool.run(inp)
            traj.add_step(subgoal=None, tool=tool.name, input=inp, output=res.output, error=res.error)
            if task.validate():
                traj.success = True
                break
        else:
            traj.success = False
        return traj

# need utility for listing
from ..tools.registry import all_tools as get_all
