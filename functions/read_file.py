import os

from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.syntax import Syntax
from rich.json import JSON
console = Console()
def read_file(base_dir="", target_file=None):
    
    console.print(f"@-reading {target_file} file data...", style="bold green")
    file_path = ""
    result = ""
    
    base_path = os.path.abspath(base_dir)
   
    file_path = os.path.join(base_path,target_file)
    print(file_path)
  
      


   
   
    print("hello ",file_path,"hello",target_file)
    

    if not file_path.startswith(base_path):
        return f"Error: {target_file} is outside {base_dir}"
    if not os.path.isfile(target_file):  return f"Error: {target_file} is not a file"
    try:
        with open(file_path,"r") as f:
             file_content = f.read()
       
        return file_content
    except Exception as e:
          result = f"-this error occured while getting file info Error:{e}"
          return result

