from __future__ import annotations
from typing import List, Dict
import os
import json

from ..env.tasks import load_tasks, Task
from ..agent.react_baseline import ReactAgent
from ..agent.adaptive_agent import AdaptiveAgent
from ..agent.planner import Planner
from ..llm.mock import MockLLM
from .metrics import summarize


def run_agents(agent_names: List[str], seed: int = 0, noise: float = 0.0) -> Dict[str, Dict]:
    tasks = load_tasks()
    results: Dict[str, Dict] = {}
    llm = MockLLM(seed, noise)
    for name in agent_names:
        trajs = []
        for t in tasks:
            if name == "react":
                agent = ReactAgent(llm)
            elif name == "plan":
                agent = AdaptiveAgent(llm)  # reuse plan-only by disabling replans
            elif name == "adaptive":
                agent = AdaptiveAgent(llm)
            else:
                continue
            traj = agent.run(t, seed=seed, noise=noise)
            trajs.append(traj)
        results[name] = summarize(trajs)
    return results


def save_report(report: Dict, path: str):
    with open(path, "w") as f:
        for agent, stats in report.items():
            f.write(f"## {agent}\n")
            for k,v in stats.items():
                f.write(f"- {k}: {v}\n")
            f.write("\n")

