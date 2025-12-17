from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt

console = Console()

def show_banner():
    title = Text("CODEAI", style="bold cyan")
    subtitle = Text(
        "My test • Tool-Driven • Local-First AI Assistant",
        style="italic bright_black"
    )

    body = Align.center(
        Text.assemble(
            ("Your intelligent code companion\n", "white"),
            ("Built for safety, clarity, and power.\n\n", "bright_black"),
            ("What Lets ", "white"),
            ("Get " ),
            ("Started.", "bold green"),
        ),
        vertical="middle",
    )

    panel = Panel(
        body,
        title=title,
        subtitle=subtitle,
        border_style="cyan",
        padding=(1, 4),
    )

    console.print(panel)
show_banner()


def get_user_input():
    return Prompt.ask(
        "[bold cyan]codeai[/bold cyan] [bright_black]❯[/bright_black]"
    )

get_user_input()