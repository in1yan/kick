from pydantic_ai import Agent
from prompts import SYSTEM_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("MODEL")

if not MODEL:
    raise Exception("Setup a proper Model")

agent = Agent(
    model=MODEL,
    system_prompt=SYSTEM_PROMPT,
    retries=3,
)
