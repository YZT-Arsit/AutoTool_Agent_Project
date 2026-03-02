from __future__ import annotations
import os
import sqlite3
from typing import Any, Dict

DATA_DIR = os.path.abspath(os.path.join(os.getcwd(), "data"))
DB_PATH = os.path.join(DATA_DIR, "sample.db")


def file_exists(params: Dict[str, Any]) -> bool:
    path = params.get("path")
    target = os.path.abspath(os.path.join(DATA_DIR, path))
    return os.path.isfile(target)


def sql_has_rows(params: Dict[str, Any]) -> bool:
    query = params.get("query")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(query)
        r = cur.fetchall()
        return len(r) > 0
    except Exception:
        return False
    finally:
        conn.close()
