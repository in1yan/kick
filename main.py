import argparse
import os
from typing import List

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("API key not set, set your GEMINI_API_KEY in environment variables")

parser = argparse.ArgumentParser(description="Kick - Coding Agent")
parser.add_argument("prompt", type=str, help="Prompt for the agent")
parser.add_argument("--verbose", action="store_true", help="Turn on verbose")

args = parser.parse_args()


def generate_content(client: genai.Client, messages: List[types.Content]) -> None:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
    )
    if args.verbose:
        if response.usage_metadata is not None:
            print(f"Prompt: {messages[0].parts[0].text}")
            print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response Tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response: \n{response.text}")


if __name__ == "__main__":
    client = genai.Client(api_key=API_KEY)
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    generate_content(client, messages)
