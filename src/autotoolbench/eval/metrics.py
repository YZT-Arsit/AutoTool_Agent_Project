from __future__ import annotations
from typing import List, Dict
from ..agent.schema import Trajectory


def summarize(trajs: List[Trajectory]) -> Dict[str, Any]:
    total = len(trajs)
    success = sum(1 for t in trajs if t.success)
    avg_steps = sum(len(t.steps) for t in trajs)/total if total else 0
    avg_calls = avg_steps  # approximation
    failure_types = {}
    for t in trajs:
        if not t.success:
            for s in t.steps:
                if s.reflection:
                    failure_types[s.reflection] = failure_types.get(s.reflection,0)+1
    return {"total":total,"success_rate": success/total if total else 0,
            "avg_steps":avg_steps,"avg_calls":avg_calls,
            "failure_types":failure_types}
