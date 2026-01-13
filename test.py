import json
import os

import requests
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from functions.read_file import read_file
# from functions.write_file import write_file
from functions.run_file import run_file

from functions.get_file_info import get_file_info
from functions.write_file import write_file
from rich.panel import Panel
from rich.console import Console
from style.banner import show_banner,get_user_input
console = Console()
# from functions.run_file import run_file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
history   =  []
show_banner()

"""
docs: https://platform.openai.com/docs/guides/function-calling
"""

tools_set = {
    "read_file":read_file,
     "get_file_info":get_file_info,
      "run_file":run_file,
       "write_file":write_file,
#         "read_file":read_file
}

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
            "name": "run_file",
            "description":   """Execute a Python file inside a restricted base directory.

HOW TO USE:
- The agent must provide `target_file`, which must be a `.py` file inside `base_dir`.
- Optional `args` must be provided as a list of strings, exactly as command-line arguments.
- The tool executes the file using the Python interpreter and waits for completion.

BEHAVIOR:
- The file is executed with: python target_file <args>
- The working directory is set to base_dir.
- Standard output (stdout), standard error (stderr), and the return code are captured and returned.

SECURITY:
- Execution of files outside base_dir is strictly forbidden.
- Only `.py` files are allowed.
- The process is terminated if it exceeds 600 seconds.

OUTPUT:
- Returns a structured result containing status, stdout, stderr, and return_code.
- If execution fails, a clear error message is returned.

The agent must not guess file contents or arguments. If required information is missing, it must refuse to call the tool.
""",
        "parameters": {
    "type": "object",
    "properties": {
        "base_dir": {
            "type": "string",
            "description": "The base directory within which execution is allowed. Defaults to the current working directory ('.')."

        },
        "target_file": {
            "type": "string",
             "description": "The Python (.py) file to execute. Must exist inside the base directory."
        }
    },
      "args": {
  "type": "array",
  "items": {
    "type": "string"
  },
  "description": "Optional command-line arguments passed to the Python script. Each item represents a single argument, exactly as it would appear in the terminal."},
    "required": ["base_dir","target_file"],
    "additionalProperties": False
},
"strict": True

        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_file_info",
            "description":   "Retrieve detailed information about the contents of a folder. By default, the current working directory ('.') is used as the base directory. The agent may optionally provide 'base_dir' to specify a different root directory or 'target_dir' to inspect a subfolder inside 'base_dir'. The function returns a list of all items in the target directory, including their full path, size in bytes, and whether they are directories. It enforces a security check so the agent cannot access paths outside the base directory. If the folder is empty or an error occurs, it returns an informative message. The agent can use this function to explore folders, verify contents, or gather metadata before performing further actions.",
        "parameters": {
    "type": "object",
    "properties": {
        "base_dir": {
            "type": "string",
        },
        "target_dir": {
            "type": "string",
        }
    },
    "required": ["base_dir","target_dir"],
    "additionalProperties": False
},
"strict": True

        },
    }
    ,

       {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file safely. By default, the current working directory ('.') is used as the base directory. The agent can optionally provide 'base_dir' to specify a different root directory. The 'target_file' parameter specifies the file to read inside the base directory. The function will return the full contents of the file as a string. It performs a security check to ensure the file is located inside 'base_dir' to prevent unauthorized access. If the file does not exist or is not a valid file, the function returns an informative error message. The agent can use this function to inspect file contents before performing further actions or making decisions based on the data.",
            "parameters": {
                "type": "object",
                "properties":  {
        "base_dir": {
            "type": "string",
        },
        "target_file": {
            "type": "string",
        }
    },
                "required": ["base_dir", "target_file"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    
       {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": """Write or overwrite a file inside a restricted base directory.

HOW TO PROVIDE CONTENT:
- The `content` parameter MUST contain the full, final contents of the file as a single string.
- Always include all lines of the file exactly as they should appear after writing.
- Do NOT provide partial edits, diffs, patches, or instructions.
- Do NOT assume any existing file contents.

BEHAVIOR:
- If the file does not exist, it will be created.
- If the file exists, it will be fully overwritten only when overwrite=true.
- If backup=true and the file exists, a backup copy is created before writing.
- The tool writes the content exactly as provided, without modification.

SECURITY:
- Access outside base_dir is strictly forbidden.
- The tool will reject paths that escape base_dir.

The agent must always explicitly pass the full file content using the `content` argument.
""",
            "parameters": {
                "type": "object",
                "properties":  {
        "base_dir": {
            "type": "string",
        },
        "target_file": {
            "type": "string",
        },
          "content": {
            "type": "string",
        }
    },
                "required": ["base_dir", "target_file","content"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }


    
]
system_prompt = """
You are an autonomous AI agent specialized in coding, file
 management, and file manipulation. You have the responsibility 
 and authority to make decisions on how to achieve tasks assigned
   to you. You must plan, prioritize, and take actions to accomplish
     tasks safely and efficiently within the allowed directories. 
     You can create, read, modify, and execute Python files, and you
       can also write additional supporting files if necessary.
         However, you can only execute Python files; you cannot 
         execute other types of files.

TOOLS AVAILABLE:

1. get_file_info(base_dir, target_dir)
   - Retrieves detailed metadata about a folder and its contents.
   - Default base directory is '.', target_dir is optional.
   - Returns full path, size in bytes, and whether each item is a directory.
   - Security: You cannot access directories outside base_dir.

2. read_file(base_dir, target_file)
   - Reads the contents of a file safely.
   - Default base directory is '.', target_file is required.
   - Returns the full contents of the file as a string.
   - Security: You cannot read files outside base_dir.

3. write_file(base_dir, target_file, content, overwrite=False, backup=False)
   - Write or overwrite a file inside a restricted base directory.
   - `content` must contain the full, final contents of the file.
   - If the file does not exist, it is created.
   - If the file exists and overwrite=True, it will be fully overwritten.
   - If backup=True and the file exists, a backup copy is created.
   - Security: Access outside base_dir is forbidden.

4. execute_python_file(base_dir, target_file, args=[])
   - Executes a `.py` file inside a restricted base directory.
   - Optional args must be a list of strings, exactly as command-line arguments.
   - Only `.py` files are allowed.
   - Execution is terminated if it exceeds 600 seconds.
   - Returns structured results containing status, stdout, stderr, and return_code.

BEHAVIOR AND DECISION-MAKING:

- You are autonomous: you must decide the best sequence of actions to achieve the assigned task.
- You may create additional Python or text files if needed to support the main task.
- You must plan your actions explicitly and provide reasoning if multiple approaches exist.
- Always validate the existence of files or directories before performing actions.
- Do not guess the contents of files; use the tools to inspect or read them.
- You may break complex tasks into smaller steps and execute them sequentially.
- When executing Python files, you must ensure safety and stay within the base_dir.

RULES FOR SAFE USAGE:

- Never access or modify files outside the allowed base directories.
- Only use each tool for its intended purpose.
- Always provide all required parameters explicitly; do not guess.
- Return clear, descriptive error messages if an operation fails.
- Use defaults safely for optional arguments when not provided by the user.
- Explicitly call tools with all necessary arguments and follow the instructions precisely.
- Always prioritize safety, accuracy, and reliability over speed.

You must strictly follow these rules to avoid errors or unsafe operations while exercising autonomous decision-making.
"""

userinput = ""
messages = [
    {"role": "system", "content": system_prompt},
    
]
while True:
    
    MAX_ITERATIONS = 10  
    userinput = get_user_input()
    messages.append({"role": "user", "content": userinput})
    iteration = 0
    while iteration < MAX_ITERATIONS:
        iteration += 1
    
    
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )
        assistant_msg = completion.choices[0].message
        messages.append(assistant_msg)

     



        def call_function(name: str, args: dict):
            if name not in tools_set:
                return {"status": "error", "error": f"Tool '{name}' not found"}
        
            try:
                result = tools_set[name](**args)
                print(f"[Tool Output] {name}: {result}")  # Optional: Rich print later
                return result
            except Exception as e:
                return {"status": "error", "error": str(e), "tool": name}
                

        tool_calls = completion.choices[0].message.tool_calls or []
        
        


        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = call_function(name, args)
            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
            )




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



        final_response = completion_2.choices[0].message.parsed
        final_response = completion_2.choices[0].message.parsed

        if final_response == None:
            console.print(Panel("can you retype your qestion something when wrong", title="[green]Details[/green]", expand=True))
        else:
            if final_response.details:
                console.print(Panel(final_response.details, title="[green]Details[/green]", expand=True))

            if final_response.message:
                console.print(Panel(final_response.message, title="[magenta]Message[/magenta]", expand=True,border_style="cyan"))
                
            console.print("[bold cyan]==================================[/bold cyan]\n")
        if len(tool_calls) ==0 and iteration >2:
            console.print(Panel(f"{len(tool_calls)}", title="[green]Details[/green]", expand=True))
            break