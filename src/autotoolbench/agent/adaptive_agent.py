from __future__ import annotations
from typing import Any, Dict, List

from .planner import Planner
from .executor import Executor
from .reflector import Reflector
from .budget import BudgetController
from .schema import Trajectory
from ..env.tasks import Task

class AdaptiveAgent:
    def __init__(self, llm, budget: BudgetController = None,
                 disable_reflector: bool = False,
                 disable_budget: bool = False,
                 disable_replan: bool = False):
        self.llm = llm
        self.planner = Planner(llm)
        self.executor = Executor()
        self.reflector = Reflector() if not disable_reflector else None
        self.budget_ctrl = (BudgetController() if not disable_budget else BudgetController(max_calls=9999,max_steps=9999))
        self.max_replans = 0 if disable_replan else 2
        self.disable_reflector = disable_reflector
        self.disable_budget = disable_budget
        self.disable_replan = disable_replan

    def run(self, task: Task, seed: int = 0, noise: float = 0.0) -> Trajectory:
        budget = self.budget_ctrl.initial()
        plan = self.planner.plan(task.instruction)
        traj = Trajectory(task_id=task.task_id)
        replans = 0
        while True:
            for step in plan:
                if not self.budget_ctrl.check(budget):
                    traj.success = False
                    return traj
                res = self.executor.execute(task.task_id, [step], budget)
                # merge step
                traj.steps.extend(res.steps)
                # validation after each
                if task.validate():
                    traj.success = True
                    return traj
                # reflect
                issue = None
                if self.reflector:
                    issue = self.reflector.classify(res.steps[-1].model_dump())
                    traj.steps[-1].reflection = issue
                if issue in ("PLAN_ERROR","MISSING_PREREQ") and replans < self.max_replans:
                    replans +=1
                    plan = self.planner.plan(task.instruction + " revise")
                    for s in plan:
                        s["replanned"] = True
                    break
            else:
                traj.success = False
                return traj
