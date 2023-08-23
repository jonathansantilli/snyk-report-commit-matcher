import os
import unittest
import json
from utils import (
    read_lines_from_file,
    get_code_path,
    read_json_file,
    get_project_dir,
    dir_exists,
    file_exists,
)


class TestFileFunctions(unittest.TestCase):

    def test_read_lines_from_file(self):
        # Create a temporary utils with some lines
        temp_file_path = "temp_file.txt"
        with open(temp_file_path, 'w', encoding='utf-8') as file:
            file.write("Line 1\nLine 2\nLine 3")

        lines = read_lines_from_file(temp_file_path)

        # Check if the lines were read correctly
        self.assertEqual(lines, ["Line 1\n", "Line 2\n", "Line 3"])

        # Clean up temporary utils
        os.remove(temp_file_path)

    def test_get_code_path(self):
        project_dir = "/path/to/project"
        code_location = "src/main/java/utils.java"

        code_path = get_code_path(project_dir, code_location)

        # Check if the code path is correctly joined
        self.assertEqual(code_path, "/path/to/project/src/main/java/utils.java")

    def test_read_json_file(self):
        # Create a temporary JSON utils with some data
        temp_json_file_path = "temp_json_file.json"
        data = {"key": "value"}
        with open(temp_json_file_path, 'w') as json_file:
            json.dump(data, json_file)

        loaded_data = read_json_file(temp_json_file_path)

        # Check if the JSON data was loaded correctly
        self.assertEqual(loaded_data, data)

        # Clean up temporary JSON utils
        os.remove(temp_json_file_path)

    def test_get_project_dir(self):
        repo_url = "https://github.com/example/repo"

        project_dir = get_project_dir(repo_url)

        # Check if the project directory is correctly formed
        self.assertEqual(project_dir, "projects/example/repo")

    def test_dir_exists(self):
        existing_directory = "tests/fixtures"

        exists = dir_exists(existing_directory)

        # Check if the existing directory is detected
        self.assertTrue(exists)

    def test_file_exists(self):
        existing_file = "tests/fixtures/snyk_report.json"

        exists = file_exists(existing_file)

        # Check if the existing utils is detected
        self.assertTrue(exists)
