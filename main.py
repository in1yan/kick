import asyncio
import os
import argparse

from functions.read import read
from functions.ls import ls
from functions.write import write
from functions.edit import edit
from agent import agent


parser = argparse.ArgumentParser(description="Kick - Coding Agent")
parser.add_argument("prompt", type=str, nargs="?", help="Prompt for the agent")
parser.add_argument("--verbose", action="store_true", help="Turn on verbose")

args = parser.parse_args()


async def main():
    message_history = []
    while True:
        prompt = input(":> ") if not args.prompt else args.prompt
        if prompt.strip() == "/exit":
            break
        async with agent.run_stream(
            prompt, deps=os.getcwd(), message_history=message_history
        ) as stream:
            async for message in stream.stream_text(delta=True):
                print(message, end="", flush=True)
            message_history = stream.all_messages()
        print()
        if args.prompt:
            break


if __name__ == "__main__":
    asyncio.run(main())
