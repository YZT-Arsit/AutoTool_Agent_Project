from __future__ import annotations
import json
from typing import Any, Dict, List

from . import validators

TASK_FILE = "data/tasks.jsonl"

class Task:
    def __init__(self, data: Dict[str, Any]):
        self.task_id = data["task_id"]
        self.instruction = data["instruction"]
        self.expected_artifacts = data.get("expected_artifacts", [])
        self.validator = data.get("validator")
        self.validator_params = data.get("validator_params", {})

    def validate(self) -> bool:
        if not self.validator:
            return False
        fn = getattr(validators, self.validator)
        return fn(self.validator_params)


def load_tasks() -> List[Task]:
    tasks: List[Task] = []
    with open(TASK_FILE) as f:
        for line in f:
            if line.strip():
                tasks.append(Task(json.loads(line)))
    return tasks


def get_task(task_id: str) -> Task | None:
    for t in load_tasks():
        if t.task_id == task_id:
            return t
    return None
