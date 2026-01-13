import os
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.syntax import Syntax
from rich.json import JSON
console = Console()


def get_file_info(base_dir="", target_dir=None):

    console.print(f"@-getting {base_dir} file info...", style="bold green")
    target_path = ""
    
    base_path = os.path.abspath(base_dir)
    if target_dir is None:
        target_path =base_path
    else:
         target_path = os.path.join(base_path,target_dir)
  
      

 
   
    result = ""

    if not target_path.startswith(base_path):
        return f"Error: {target_dir} is outside {base_dir}"
    try:
        contents = os.listdir(target_path)
      
        if len(contents) == 0:return f"{base_path} folder is empty"
        for content in contents :
            console.print("-",content, style="bold green")
            content_path = os.path.join(target_path,content)
            size = os.path.getsize(content_path)
            is_dir = os.path.isdir(content_path)
       
        
            result += f" -path:{content_path} -- size:{size}byte -- isdir:{is_dir}\n"
        return result
    except Exception as e:
          result = f"-this error occured while getting file info Error:{e}"
          return result


