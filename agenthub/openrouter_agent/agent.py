from __future__ import annotations

from typing import Dict, List

from opendevin.agent import Agent
from opendevin.llm.llm import LLM
from opendevin.action import Action
from opendevin.state import State

from agenthub.monologue_agent.agent import MonologueAgent
from agenthub.codeact_agent.codeact_agent import CodeActAgent
from agenthub.SWE_agent.agent import SWEAgent
from agenthub.planner_agent.agent import PlannerAgent


class OpenRouterAgent(Agent):
    """Routes tasks to specialized agents using OpenRouter-backed LLMs."""

    def __init__(self, llm: LLM):
        super().__init__(llm)
        # Initialize sub-agents with dedicated models
        self.agents: Dict[str, Agent] = {
            'monologue': MonologueAgent(
                LLM(model='gpt-3.5-turbo', api_key=llm.api_key, base_url=llm.base_url)
            ),
            'code': SWEAgent(
                LLM(model='gpt-4', api_key=llm.api_key, base_url=llm.base_url)
            ),
            'planner': PlannerAgent(
                LLM(model='gpt-3.5-turbo', api_key=llm.api_key, base_url=llm.base_url)
            ),
            'shell': CodeActAgent(
                LLM(model='gpt-4', api_key=llm.api_key, base_url=llm.base_url)
            ),
        }
        self.current_agent: Agent | None = None

    def select_agent(self, task: str) -> Agent:
        """Select an agent based on the task description."""
        task_l = task.lower()
        if any(k in task_l for k in ['code', 'bug', 'implement', 'write', 'fix', 'develop']):
            return self.agents['code']
        if any(k in task_l for k in ['plan', 'roadmap', 'strategy']):
            return self.agents['planner']
        if any(k in task_l for k in ['shell', 'command', 'bash']):
            return self.agents['shell']
        return self.agents['monologue']

    def step(self, state: State) -> Action:
        if self.current_agent is None:
            self.current_agent = self.select_agent(state.plan.main_goal)
        return self.current_agent.step(state)

    def search_memory(self, query: str) -> List[str]:
        results: List[str] = []
        for agent in self.agents.values():
            try:
                results.extend(agent.search_memory(query))
            except Exception:
                continue
        return results

    def reset(self) -> None:
        for agent in self.agents.values():
            agent.reset()
        self.current_agent = None
        super().reset()
