from __future__ import annotations
import os
from .runner import save_report

REPORT_DIR = "reports"


def generate(report: Dict):
    if not os.path.isdir(REPORT_DIR):
        os.makedirs(REPORT_DIR, exist_ok=True)
    path = os.path.join(REPORT_DIR, "latest_report.md")
    save_report(report, path)
    return path
