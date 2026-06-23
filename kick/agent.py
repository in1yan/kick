from pydantic_ai import Agent, Tool
from kick.prompts import SYSTEM_PROMPT
from kick.functions.bash import bash
from kick.functions.edit import edit
from kick.functions.ls import ls
from kick.functions.read import read
from kick.functions.write import write


def create_agent(cf):
    MODEL = cf.agent.model
    tools = [bash, edit, ls, write, read]

    if not MODEL:
        raise Exception("Setup a proper Model")
    agent = Agent(
        model=MODEL,
        system_prompt=SYSTEM_PROMPT,
        retries=3,
        tools=[
            Tool(ls, takes_ctx=True),
            Tool(read, takes_ctx=True),
            Tool(write, takes_ctx=True),
            Tool(edit, takes_ctx=True),
            Tool(bash, takes_ctx=True),
        ],
    )
    return agent
