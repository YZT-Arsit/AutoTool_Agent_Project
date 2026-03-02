#!/bin/bash
if [ -z "$1" ]; then
echo "usage: $0 TASK_ID"; exit 1; fi
python -m autotoolbench.run --task-id "$1" --agent adaptive
