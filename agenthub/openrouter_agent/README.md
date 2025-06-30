# OpenRouter Agent

This agent coordinates multiple sub-agents and routes requests to the best LLM model available through the OpenRouter service.
It dynamically selects between a coding specialist, planner, shell agent, or the default monologue agent based on the task description.
Each sub-agent runs on its own LLM model allowing optimized performance for different workloads.

## Configuration

Set your OpenRouter credentials using the standard LLM variables:

```bash
export LLM_API_KEY="<your-openrouter-api-key>"
export LLM_BASE_URL="https://openrouter.ai/api/v1"
```

## Example

Instantiate the agent in Python with a configured `LLM`:

```python
from agenthub.openrouter_agent import OpenRouterAgent
from opendevin.llm.llm import LLM

llm = LLM(api_key="<your-openrouter-api-key>", base_url="https://openrouter.ai/api/v1")
agent = OpenRouterAgent(llm)
```
