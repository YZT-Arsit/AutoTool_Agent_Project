from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import time

class StepRecord(BaseModel):
    timestamp: float
    subgoal: Optional[str]
    tool: Optional[str]
    input: Dict[str, Any]
    output: Any = None
    error: Optional[str] = None
    reflection: Optional[str] = None
    replanned: bool = False
    budget: Dict[str, Any] = {}

class Trajectory(BaseModel):
    task_id: str
    steps: List[StepRecord] = []
    success: Optional[bool] = None

    def add_step(self, **kwargs):
        kwargs.setdefault('timestamp', time.time())
        self.steps.append(StepRecord(**kwargs))
