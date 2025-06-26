from agenthub.openrouter_agent.agent import OpenRouterAgent
from agenthub.SWE_agent.agent import SWEAgent
from agenthub.planner_agent.agent import PlannerAgent
from opendevin.llm.llm import LLM
from opendevin.plan import Plan
from opendevin.state import State


def test_select_agent_code():
    llm = LLM(model='gpt-3.5-turbo')
    agent = OpenRouterAgent(llm)
    selected = agent.select_agent('fix the bug in this code')
    assert isinstance(selected, SWEAgent)


def test_select_agent_plan():
    llm = LLM(model='gpt-3.5-turbo')
    agent = OpenRouterAgent(llm)
    selected = agent.select_agent('create a roadmap for project')
    assert isinstance(selected, PlannerAgent)


def test_step_uses_selected_agent():
    llm = LLM(model='gpt-3.5-turbo')
    agent = OpenRouterAgent(llm)
    plan = Plan('fix code')
    state = State(plan)
    # monkeypatch the underlying agent to avoid network calls
    agent.agents['code'].step = lambda s: s  # type: ignore
    result = agent.step(state)
    assert result == state
    assert isinstance(agent.current_agent, SWEAgent)
