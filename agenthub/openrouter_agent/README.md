# OpenRouter Agent

This agent coordinates multiple sub-agents and routes requests to the best LLM model available through the OpenRouter service.
It dynamically selects between a coding specialist, planner, shell agent, or the default monologue agent based on the task description.
Each sub-agent runs on its own LLM model allowing optimized performance for different workloads.
