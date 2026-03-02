#!/usr/bin/env python3
import sqlite3, os, json

def main():
    base = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base, "data")
    os.makedirs(os.path.join(data_dir, "logs"), exist_ok=True)
    # create sqlite
    db_path = os.path.join(data_dir, "sample.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cur.execute("DELETE FROM users")
    cur.executemany("INSERT INTO users (name, age) VALUES (?,?)", [("alice",30),("bob",25)])
    conn.commit(); conn.close()
    # create log
    log_path = os.path.join(data_dir, "logs/app.log")
    with open(log_path, "w") as f:
        f.write("INFO start\nERROR failed test1\nINFO processed\n")
    # create tasks
    tasks = []
    # generate 15 tasks of various types
    for i in range(1,16):
        tid = f"T{i:03d}"
        if i <=5:
            # DataOps: need to run an SQL query
            instr = "select * from users"
            if i == 1:
                instr = "select * from users and write to file report.txt"
                tasks.append({
                    "task_id": tid,
                    "instruction": instr,
                    "expected_artifacts": ["report.txt"],
                    "validator": "file_exists",
                    "validator_params": {"path": "report.txt"}
                })
                continue
            tasks.append({
                "task_id": tid,
                "instruction": instr,
                "expected_artifacts": [],
                "validator": "sql_has_rows",
                "validator_params": {"query": "SELECT * FROM users"}
            })
        elif i<=10:
            # DebugOps: search log
            tasks.append({
                "task_id": tid,
                "instruction": "search logs for ERROR",
                "expected_artifacts": [],
                "validator": "file_exists",
                "validator_params": {"path": "logs/app.log"}
            })
        else:
            # Workflow: writing a draft file
            tasks.append({
                "task_id": tid,
                "instruction": "write greeting to file email.txt",
                "expected_artifacts": ["email.txt"],
                "validator": "file_exists",
                "validator_params": {"path": "email.txt"}
            })
    tasks_path = os.path.join(base, "data/tasks.jsonl")
    with open(tasks_path, "w") as f:
        for t in tasks:
            f.write(json.dumps(t)+"\n")

if __name__ == '__main__':
    main()