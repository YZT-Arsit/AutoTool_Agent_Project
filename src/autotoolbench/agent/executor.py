from __future__ import annotations
from typing import Any, Dict, List

from .schema import Trajectory
from ..tools.registry import get

class Executor:
    def __init__(self):
        pass

    def execute(self, task_id: str, plan: List[Dict[str, Any]], budget: Dict[str, Any]) -> Trajectory:
        traj = Trajectory(task_id=task_id)
        for step in plan:
            tool_name = step.get("tool") or "noop"
            args = step.get("args", {})
            try:
                tool = get(tool_name)
            except KeyError:
                traj.add_step(subgoal=step.get("subgoal"), tool=tool_name, input=args, error="tool_not_found", budget=budget)
                continue
            res = tool.run(args)
            # budget consumption simple decrement
            budget["calls"] = budget.get("calls",0) + 1
            budget["steps"] = budget.get("steps",0) + 1
            traj.add_step(subgoal=step.get("subgoal"), tool=tool_name, input=args, output=res.output, error=res.error, budget=budget)
        traj.success = False
        return traj
