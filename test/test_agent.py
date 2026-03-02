import pytest
from autotoolbench.agent.adaptive_agent import AdaptiveAgent
from autotoolbench.llm.mock import MockLLM
from autotoolbench.env.tasks import load_tasks


def test_adaptive_agent_runs():
    import scripts.make_data as md
    md.main()
    tasks = load_tasks()
    if not tasks:
        pytest.skip("no tasks")
    llm = MockLLM(seed=0, noise=0)
    agent = AdaptiveAgent(llm)
    traj = agent.run(tasks[0])
    assert traj.task_id == tasks[0].task_id
    assert hasattr(traj, 'steps')
