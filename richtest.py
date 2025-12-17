
from functions.get_file_info import get_file_info
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.syntax import Syntax
from rich.json import JSON


console = Console()
console.print("Hello", style="bold green")
console.print("[bold red]Error:[/bold red] File not found")
from rich.panel import Panel

console.print(
    Panel("Hello world", title="Info", border_style="cyan")
)
code = "print('Hello')"
syntax = Syntax(code, "python", theme="monokai")
console.print(syntax)

