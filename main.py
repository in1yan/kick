from prompts import SYSTEM_PROMPT
import argparse
import os
from typing import List

from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function

load_dotenv(override=True)
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("API key not set, set your GEMINI_API_KEY")

parser = argparse.ArgumentParser(description="Kick - Coding Agent")
parser.add_argument("prompt", type=str, help="Prompt for the agent")
parser.add_argument("--verbose", action="store_true", help="Turn on verbose")

args = parser.parse_args()


def generate_content(
    client: genai.Client, messages: List[types.Content]
) -> tuple[types.GenerateContentResponse, List[types.Content]]:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
    )

    if args.verbose:
        if response.usage_metadata is not None:
            print(f"Prompt: {messages[0].parts[0].text}")
            print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response Tokens: {response.usage_metadata.candidates_token_count}")
    function_results = []
    if response.function_calls:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
            function_result = call_function(call)
            if not function_result.parts:
                raise Exception("The parts of the function call is empty")
            if not function_result.parts[0].function_response:
                raise Exception("No result from the function call")
            if not function_result.parts[0].function_response.response:
                raise Exception("No response from the function call")
            function_results.append(function_result.parts[0])
            if args.verbose:
                print(
                    f"-> {function_result.parts[0].function_response.response['result']}"
                )
        # print(f"Response: \n{response.text}")
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    for function_call in function_results:
        messages.append(types.Content(role="user", parts=[function_call]))
    return response, messages


if __name__ == "__main__":
    client = genai.Client(api_key=API_KEY)
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    for _ in range(20):
        resp, messages = generate_content(client, messages)
        if not resp.function_calls:
            print(f"Response: {resp.text}")
            break
