import os
import typer
from typer.testing import CliRunner
from autotoolbench.agent.budget import BudgetController
from autotoolbench.agent.reflector import Reflector
from autotoolbench.llm.mock import MockLLM
from autotoolbench.agent.planner import Planner


def test_budget_controller():
    b = BudgetController(max_calls=2, max_steps=2)
    bud = b.initial()
    assert b.check(bud)
    bud["calls"] = 2
    assert not b.check(bud)


def test_reflector():
    r = Reflector()
    assert r.classify({"error": "oops"}) == "BAD_TOOL_ARGS"
    assert r.classify({}) == "PLAN_ERROR"


def test_planner_noise():
    llm = MockLLM(seed=0, noise=1.0)
    p = Planner(llm)
    plan = p.plan("select * from users")
    # with noise=1 should corrupt query
    for step in plan:
        assert step["args"] == {}


def test_cli_run_logs(tmp_path, monkeypatch):
    # ensure data exists
    import scripts.make_data as md
    md.main()
    # run CLI with a known task
    from autotoolbench.cli import app
    runner = CliRunner()
    result = runner.invoke(app, ["run","--task-id","T001","--agent","adaptive","--seed","0","--noise","0"])
    assert result.exit_code == 0
    # check log file created
    logdir = os.path.join(os.getcwd(), "data", "logs")
    files = [f for f in os.listdir(logdir) if f.startswith("trajectory_T001")]
    assert files
