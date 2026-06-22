from pydantic_ai import Agent
from prompts import SYSTEM_PROMPT
from config import config, load_config


def create_agent(cf):
    MODEL = cf.agent.model

    if not MODEL:
        raise Exception("Setup a proper Model")
    agent = Agent(
        model=MODEL,
        system_prompt=SYSTEM_PROMPT,
        retries=3,
    )
    return agent


agent = create_agent(config)
