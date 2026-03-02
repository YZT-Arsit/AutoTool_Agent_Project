from __future__ import annotations
from typing import Dict, Any

from .runner import run_agents
from ..llm.mock import MockLLM
from ..agent.adaptive_agent import AdaptiveAgent
from ..env.tasks import load_tasks
from .metrics import summarize


def ablate(seed: int = 0, noise: float = 0.0) -> Dict[str, Dict[str, Any]]:
    # run baseline and some ablations
    tasks = []
    # baseline adaptive
    llm = MockLLM(seed, noise)
    report: Dict[str, Dict[str, Any]] = {}
    # run normal
    report["adaptive"] = run_agents(["adaptive"], seed=seed, noise=noise)["adaptive"]
    # run without reflector
    agent = AdaptiveAgent(llm, disable_reflector=True)
    # simulate by direct call on tasks inside runner variant
    # easiest: create helper
    def single_run(agent):
        trajs = []
        for t in load_tasks():
            trajs.append(agent.run(t, seed=seed, noise=noise))
        return summarize(trajs)
    report["no_reflector"] = single_run(AdaptiveAgent(llm, disable_reflector=True))
    report["no_budget"] = single_run(AdaptiveAgent(llm, disable_budget=True))
    report["no_replan"] = single_run(AdaptiveAgent(llm, disable_replan=True))
    return report
