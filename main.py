import asyncio
import os
import argparse

from functions.read import read
from functions.ls import ls
from functions.write import write
from functions.edit import edit
from agent import agent


parser = argparse.ArgumentParser(description="Kick - Coding Agent")
parser.add_argument("prompt", type=str, help="Prompt for the agent")
parser.add_argument("--verbose", action="store_true", help="Turn on verbose")

args = parser.parse_args()


async def main():
    async with agent.run_stream(args.prompt, deps=os.getcwd()) as stream:
        async for message in stream.stream_text(delta=True):
            print(message, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
