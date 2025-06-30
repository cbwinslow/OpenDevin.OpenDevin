import argparse
import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List

from opendevin.agent import Agent
from opendevin.controller import AgentController
from opendevin.llm.llm import LLM


async def run_agent(task: Dict[str, Any]) -> Dict[str, Any]:
    """Run an OpenDevin agent on a single SWE-bench task.

    Parameters
    ----------
    task: dict
        A dictionary with at least ``instance_id`` and ``instructions`` keys.

    Returns
    -------
    dict
        A prediction dictionary containing ``instance_id`` and ``model_patch``.
    """
    llm = LLM(model="gpt-3.5-turbo")
    agent_cls = Agent.get_cls("SWEAgent")
    agent = agent_cls(llm)
    controller = AgentController(agent=agent)
    await controller.start_loop(task["instructions"])

    return {
        "instance_id": task["instance_id"],
        "model_patch": "",  # TODO: capture diff from the agent
        "model_name_or_path": "OpenDevin",
    }


async def generate_predictions(tasks_path: str, output_path: str) -> None:
    """Run OpenDevin on a list of SWE-bench tasks and write predictions."""
    tasks: List[Dict[str, Any]] = json.loads(Path(tasks_path).read_text())
    predictions: List[Dict[str, Any]] = []
    for task in tasks:
        prediction = await run_agent(task)
        predictions.append(prediction)

    Path(output_path).write_text(json.dumps(predictions, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks_path", help="Path to SWE-bench tasks JSON file")
    parser.add_argument("output_path", help="File to write predictions JSON")
    args = parser.parse_args()

    asyncio.run(generate_predictions(args.tasks_path, args.output_path))
