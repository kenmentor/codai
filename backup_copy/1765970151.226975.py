import json
import os

import requests
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from functions.read_file import read_file
from functions.write_file import write_file
from functions.get_file_info import get_file_info
from functions.run_file import run_file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


"""
docs: https://platform.openai.com/docs/guides/function-calling
"""

# --------------------------------------------------------------
# Define the tool (function) that we want to call
# --------------------------------------------------------------


def get_weather(latitude, longitude):
    """This is a publically available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]


# --------------------------------------------------------------
# Step 1: Call model with get_weather tool defined
# --------------------------------------------------------------
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_weather",
#             "description": "Get current temperature for provided coordinates in celsius.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "latitude": {"type": "number"},
#                     "longitude": {"type": "number"},
#                 },
#                 "required": ["latitude", "longitude"],
#                 "additionalProperties": False,
#             },
#             "strict": True,
#         },
#     }
# ]
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_file_info",
            "description": """Use this function to retrieve detailed information about the contents of a folder. 
The 'base_dir' parameter specifies the base directory from which the agent is allowed to access files.
The optional 'target_dir' parameter specifies a subfolder within 'base_dir'; if not provided, the base directory itself will be used.
The function returns a list of all items in the target directory, with their full path, size in bytes, and whether the item is a directory.
It performs a security check to ensure the agent cannot access paths outside the specified base directory.
If the folder is empty, it returns a message indicating so.
If an error occurs (e.g., folder does not exist), it returns an error message describing the problem.
The agent can use this function whenever it needs to inspect folders, verify contents, or gather metadata about files and directories before performing further actions.""",

        "parameters": {
    "type": "object",
    "properties": {
        "base_dir": {
            "type": "string",
            "description": "The base directory path where the agent is allowed to inspect files and folders. This is the root scope for security."
        },
        "target_dir": {
            "type": "string",
            "description": "Optional. A subdirectory inside base_dir to inspect. If not provided, the function will inspect the base_dir itself."
        }
    },
    "required": ["base_dir"],
    "additionalProperties": False
},
"strict": True

        },
    }
]

system_prompt = "you are a helpfull file manager assistand that can get file details."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "how many files are in the home directry"},
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# --------------------------------------------------------------
# Step 2: Model decides to call function(s)
# --------------------------------------------------------------

completion.model_dump()

# --------------------------------------------------------------
# Step 3: Execute get_weather function
# --------------------------------------------------------------


def call_function(name, args):
    if name == "get_file_info":
        return get_file_info(**args)


for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )

# --------------------------------------------------------------
# Step 4: Supply result and call model again
# --------------------------------------------------------------


class FileInfoResponse(BaseModel):
    details: str = Field(
        description="A detailed string containing information about each item in the directory. "
                    "For each file or folder, it includes the full path, size in bytes, and whether it is a directory."
    )
    message: str = Field(
        description="A natural language summary or status message describing the result of the operation. "
                    "For example, it can indicate that the folder is empty or that an error occurred."
    )
completion_2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=FileInfoResponse,
)

# --------------------------------------------------------------
# Step 5: Check model response
# --------------------------------------------------------------

final_response = completion_2.choices[0].message.parsed
print(final_response.temperature,
final_response.response)