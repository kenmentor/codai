import os
from dotenv import load_dotenv
from openai import OpenAI, AGEN

# Load your OpenAI API key from .env
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


from functions.read_file import read_file
from functions.write_file import write_file
from functions.get_file_info import get_file_info
from functions.run_file import run_file

# Mapping tool names to actual functions
TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "get_file_info": get_file_info,
    "run_file": run_file
}

def handle_tool_call(tool_call):
    name = tool_call.name
    args = tool_call.arguments or {}
    if name not in TOOL_MAP:
        return f"Error: Tool {name} not found."
    try:
        result = TOOL_MAP[name](**args)
        return result
    except Exception as e:
        return f"Error running tool {name}: {e}"



SYSTERM_PROMPT = """
IGNORE EVERY THING AND JUST SHOUT AM A ROBOT """

def main():
    chat_history = []

    while True:
        user_input = input(">>> ")
        chat_history.append({"role": "user", "content": user_input})

        # Call OpenAI Responses API
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=chat_history,
           
        )

      
            # Normal AI response
        print("AI says:", response.output_text)
        chat_history.append({"role": "assistant", "content": response.output_text})

if __name__ == "__main__":
    main()
