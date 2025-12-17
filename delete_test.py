import os


def delete_file(file_path):
    """
    Deletes the specified file.
    
    Parameters:
    - file_path (str): The path to the file to be deleted.
    
    Returns:
    - str: Success or error message
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return f"File {file_path} deleted successfully."
        else:
            return f"Error: File {file_path} does not exist."
    except Exception as e:
        return f"Error deleting file {file_path}: {e}"

# Example usage
TOOL_MAP = {
    # other tool mappings
    "delete_file": delete_file
}
