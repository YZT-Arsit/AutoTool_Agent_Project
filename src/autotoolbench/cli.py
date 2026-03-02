from __future__ import annotations
import typer
import json

from .env import tasks as tasksmod
from .eval import runner, report, ablation
from .llm.mock import MockLLM
from .agent.react_baseline import ReactAgent
from .agent.adaptive_agent import AdaptiveAgent

app = typer.Typer()

@app.command()
def make_data():
    """Generate sample database, logs, and tasks"""
    import scripts.make_data as md
    md.main()
    typer.echo("data generated")

@app.command()
def run(
    task_id: str = typer.Option(..., "--task-id", help="ID of the task to run"),
    agent: str = "adaptive",
    seed: int = 0,
    noise: float = 0.0,
):
    """Run a single task with given agent"""
    t = tasksmod.get_task(task_id)
    if not t:
        typer.echo(f"task {task_id} not found")
        raise typer.Exit(code=1)
    llm = MockLLM(seed, noise)
    if agent == "react":
        ag = ReactAgent(llm)
    else:
        ag = AdaptiveAgent(llm)
    traj = ag.run(t, seed=seed, noise=noise)
    # persist trajectory for later analysis
    import os
    logdir = os.path.join(os.getcwd(), "data", "logs")
    os.makedirs(logdir, exist_ok=True)
    fname = f"trajectory_{task_id}_{seed}.json"
    with open(os.path.join(logdir, fname), "w") as lf:
        lf.write(traj.model_dump_json(indent=2))
    typer.echo(traj.model_dump_json(indent=2))
    typer.echo(f"trajectory written to {os.path.join(logdir, fname)}")

@app.command()
def eval(agent: str = "all", seed: int = 0, noise: float = 0.0):
    """Run evaluation"""
    if agent == "all":
        names = ["react","plan","adaptive"]
    else:
        names = [agent]
    res = runner.run_agents(names, seed=seed, noise=noise)
    path = report.generate(res)
    typer.echo(f"report saved to {path}")

@app.command()
def ablate(seed: int = 0, noise: float = 0.0):
    """Run ablation"""
    res = ablation.ablate(seed=seed, noise=noise)
    path = report.generate(res)
    typer.echo(f"ablation saved to {path}")

if __name__ == "__main__":
    app()
