import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
from tkinter import Tk, Text, Scrollbar, Button, END
from functions.read_file import read_file
from functions.write_file import write_file
from functions.run_file import run_file
from functions.get_file_info import get_file_info

# Load environment variables (ensure .env file is present with proper variables)
load_dotenv()

# Initialize OpenAI client
gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Toolset for executing various file operations
tools_set = {
    "read_file": read_file,
    "write_file": write_file,
    "get_file_info": get_file_info,
    "run_file": run_file
}

# System prompt providing the rules and capabilities of the AI system
system_prompt = """
You are a specialized AI assistant focused on managing and manipulating files carefully.
You must always adhere to safety, ensuring no unauthorized file access occurs.
"""

# GUI setup using Tkinter
class AIInterface:
    def __init__(self, master):
        self.master = master
        master.title("AI Interface")

        self.text_area = Text(master, wrap='word', height=20, width=50)
        self.scroll = Scrollbar(master, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scroll.set)

        self.scroll.pack(side='right', fill='y')
        self.text_area.pack(side='top', fill='both', expand=True)

        self.toolbar = Text(master, height=1, wrap='word', state='normal')
        self.toolbar.pack(fill='x')

        self.send_button = Button(master, text="Send", command=self.send_input)
        self.send_button.pack(side='bottom', fill='x')

        self.messages = [{"role": "system", "content": system_prompt}]

    def send_input(self):
        user_input = self.toolbar.get("1.0", END).strip()
        if user_input:
            self.messages.append({"role": "user", "content": user_input})
            self.toolbar.delete("1.0", END)
            self.update_ai_response(user_input)

    def update_ai_response(self, user_input):
        response = gpt_client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages
        )
        
        assistant_output = response.choices[0].message['content']
        self.messages.append({"role": "assistant", "content": assistant_output})
        
        self.text_area.config(state='normal')
        self.text_area.insert(END, f"User: {user_input}\nAI: {assistant_output}\n")
        self.text_area.config(state='disabled')

# Function to run the Tkinter application
def run_app():
    root = Tk()
    interface = AIInterface(root)
    root.mainloop()

# Execute the application
if __name__ == "__main__":
    run_app()
