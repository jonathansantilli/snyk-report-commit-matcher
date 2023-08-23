import os
import json
from typing import Dict, List
from urllib.parse import urlparse


def read_lines_from_file(file_path: str) -> List[str]:
    """
    Read lines from a text file and return them as a list.

    Args:
        file_path (str): The path to the text file.

    Returns:
        list: A list of lines read from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def get_code_path(project_dir: str, code_location: str) -> str:
    """
    Get the full path to a code file within a project directory.

    Args:
        project_dir (str): The project directory.
        code_location (str): The location of the code file relative to the project directory.

    Returns:
        str: The full path to the code file.
    """
    return os.path.join(project_dir, code_location)


def read_json_file(file_path: str) -> Dict:
    """
   Read and parse a JSON file and return its content as a dictionary.

   Args:
       file_path (str): The path to the JSON file.

   Returns:
       dict: The parsed JSON content as a dictionary.
   """
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def get_project_dir(repo_url: str) -> str:
    """
    Get the project directory path based on a repository URL.

    Args:
        repo_url (str): The URL of the repository.

    Returns:
        str: The path to the project directory.
    """
    project_path = urlparse(repo_url).path
    return os.path.join('projects', project_path[1: len(project_path)])


def dir_exists(directory_name: str) -> bool:
    """
    Check if a directory exists.

    Args:
        directory_name (str): The name of the directory to check.

    Returns:
        bool: True if the directory exists, False otherwise.
    """
    return os.path.isdir(directory_name)


def file_exists(file_name: str) -> bool:
    """
    Check if a file exists.

    Args:
        file_name (str): The name of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_name)
