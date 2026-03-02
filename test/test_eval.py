import pytest
from autotoolbench.eval.runner import run_agents
from autotoolbench.eval.ablation import ablate


def test_runner():
    res = run_agents(["react"], seed=0, noise=0)
    assert "react" in res
    assert isinstance(res['react']['success_rate'], float)


def test_ablation():
    res = ablate(seed=0, noise=0)
    assert 'adaptive' in res
