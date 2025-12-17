import os
import subprocess
from typing import List

def run_file(
    base_dir: str = ".",
    target_file: str | None = None,
    args: List[str] = []
):
    if not target_file:
        return {
            "status": "error",
            "error": "target_file is required"
        }

    # Resolve absolute paths
    base_path = os.path.abspath(base_dir)
    file_path = os.path.abspath(os.path.join(base_path, target_file))

    # Security: prevent directory escape
    if not file_path.startswith(base_path):
        return {
            "status": "error",
            "error": "Access denied: target_file is outside base_dir"
        }

    # Validation
    if not os.path.isfile(file_path):
        return {
            "status": "error",
            "error": "target_file does not exist or is not a file",
            "file": target_file
        }

    if not file_path.endswith(".py"):
        return {
            "status": "error",
            "error": "Only Python (.py) files can be executed",
            "file": target_file
        }

    try:
        command = ["python", file_path] + list(args)

        result = subprocess.run(
            command,
            cwd=base_path,
            timeout=600,
            capture_output=True,
            text=True
        )

        return {
            "status": "success" if result.returncode == 0 else "error",
            "file": target_file,
            "args": args,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error": "Execution timed out (600s limit)",
            "file": target_file
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "file": target_file
        }
