import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()

def write_file(
    base_dir: str = ".",
    target_file: str | None = None,
    content: str = "",
    overwrite: bool = True,
    create_dirs: bool = True,
    backup: bool = True
):
    """
    Safely write or overwrite a file inside base_dir.
    Designed for LLM tool usage.
    """

    if not target_file:
        return {
            "status": "error",
            "error": "target_file is required"
        }

    base_path = os.path.abspath(base_dir)
    file_path = os.path.abspath(os.path.join(base_path, target_file))
    backup_dir = os.path.join(base_path, ".backup")

    # 🔒 Security check
    if not file_path.startswith(base_path):
        return {
            "status": "error",
            "error": "Access denied: target_file is outside base_dir"
        }

    file_existed = os.path.isfile(file_path)

    if file_existed and not overwrite:
        return {
            "status": "error",
            "error": "File exists and overwrite is disabled",
            "file": target_file
        }

    try:
        # Ensure parent directories
        parent_dir = os.path.dirname(file_path)
        if create_dirs and not os.path.isdir(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        backup_created = False

        # Backup old file if it exists
        if backup and file_existed:
            os.makedirs(backup_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(
                backup_dir,
                f"{os.path.basename(target_file)}.{timestamp}.bak"
            )
            with open(file_path, "r", encoding="utf-8") as f:
                old_content = f.read()
            with open(backup_path, "w", encoding="utf-8") as bf:
                bf.write(old_content)
            backup_created = True

        # Write content
        with open(file_path, "w", encoding="utf-8") as f:
            chars_written = f.write(content)

        console.print(
            Panel.fit(
                f"[bold green]WRITE SUCCESS[/bold green]\n"
                f"[white]File:[/white] {target_file}\n"
                f"[white]Mode:[/white] {'overwrite' if file_existed else 'new file'}\n"
                f"[white]Characters:[/white] {chars_written}",
                title="CodeAI",
            )
        )

        return {
            "status": "success",
            "file": target_file,
            "characters_written": chars_written,
            "overwritten": file_existed,
            "backup_created": backup_created
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "file": target_file
        }
