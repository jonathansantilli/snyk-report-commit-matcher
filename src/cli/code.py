from typing import List

from report import SarifReport, CodeRegion
from utils import read_lines_from_file, get_code_path


class InvalidLineException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidContentException(Exception):
    def __init__(self, message):
        super().__init__(message)


class CodeReport:
    def __init__(self, code_file_path: str, code_region: CodeRegion, line_content: str):
        """
        Initializes a CodeReport object.

        Args:
            code_file_path (str): The path to the code file.
            code_region (CodeRegion): The code region specifying start and end positions.
            line_content (str): The content of the code line within the specified region.
        """
        self.code_file_path = code_file_path
        self.code_region = code_region
        self.line_content = line_content

    def to_string(self):
        """
        Returns a string representation of the CodeReport object.

        Returns:
            str: A string representation in the format:
                "<code_file_path>::<start_line>::<end_line> <start_column-1>-><end_column> = <line_content>"
        """
        return f"{self.code_file_path}::" \
               f"{self.code_region.start_line}::" \
               f"{self.code_region.end_line} " \
               f"{self.code_region.start_column - 1}->{self.code_region.end_column} " \
               f"= {self.line_content}"


def process_source_code(project_dir: str, sarif_report: SarifReport) -> List[CodeReport]:
    """
    Processes a Snyk Code report and extracts code regions.

    Args:
        project_dir (str): The project directory path.
        sarif_report (SarifReport): The Snyk Code report to process.

    Returns:
        List[CodeReport]: A list of CodeReport objects representing code regions.
    """
    report: List[CodeReport] = []

    def process(artifact_location_uri: str, region: CodeRegion) -> CodeReport:
        path = get_code_path(project_dir, artifact_location_uri)
        code_snippet_report = read_code_snippet(path, region)
        if starts_with_space(code_snippet_report.line_content):
            raise InvalidContentException(f"Invalid line content: {code_snippet_report.line_content}")

        return code_snippet_report

    for run in sarif_report.runs:
        for result in run.results:
            report += [process(location.artifact_location_uri, location.region) for location in result.locations]
            for code_flow in result.code_flows:
                for thread_flow in code_flow.thread_flows:
                    report += [process(thread_location.artifact_location_uri, thread_location.region)
                               for thread_location in thread_flow.locations]

    return report


def read_code_snippet(code_file_path: str, code_region: CodeRegion) -> CodeReport:
    """
    Reads a code snippet from a code file based on the provided CodeRegion.

    Args:
        code_file_path (str): The path to the code file.
        code_region (CodeRegion): The code region specifying start and end positions.

    Returns:
        CodeReport: A CodeReport object representing the code snippet.
    """
    is_multi_line = code_region.start_line != code_region.end_line

    if is_multi_line:
        # The code expands to more than one line
        return read_multiple_line_code_snippet(code_file_path, code_region)

    return read_single_line_code_snippet(code_file_path, code_region)


def read_single_line_code_snippet(code_file_path: str, code_region: CodeRegion) -> CodeReport:
    """
    Reads a single-line code snippet from a code file based on the provided CodeRegion.

    Args:
        code_file_path (str): The path to the code file.
        code_region (CodeRegion): The code region specifying start and end positions.

    Returns:
        CodeReport: A CodeReport object representing the single-line code snippet.
    """
    file_lines = read_lines_from_file(code_file_path)

    if len(file_lines) < code_region.end_line:
        throw_invalid_number_of_lines_exception(code_file_path, len(file_lines), code_region.end_line)

    line_number = code_region.start_line - 1
    line = file_lines[line_number]

    if len(line) < code_region.end_column:
        throw_invalid_line_length_exception(code_file_path, line_number, len(line), code_region.end_column)

    start_column = code_region.start_column - 1
    end_column = code_region.end_column

    return CodeReport(code_file_path, code_region, line[start_column:end_column])


def read_multiple_line_code_snippet(code_file_path: str, code_region: CodeRegion) -> CodeReport:
    """
    Reads a multi-line code snippet from a code file based on the provided CodeRegion.

    Args:
        code_file_path (str): The path to the code file.
        code_region (CodeRegion): The code region specifying start and end positions.

    Returns:
        CodeReport: A CodeReport object representing the multi-line code snippet.
    """
    file_lines = read_lines_from_file(code_file_path)

    if len(file_lines) < code_region.end_line:
        throw_invalid_number_of_lines_exception(code_file_path, len(file_lines), code_region.end_line)

    code_lines: List[str] = []
    end_column = 0

    for line_number in range(code_region.start_line - 1, code_region.end_line):
        line = file_lines[line_number]
        code_lines.append(line)
        # Is the last line?
        if line_number == (code_region.end_line - 1):
            if len(line) < code_region.end_column:
                throw_invalid_line_length_exception(code_file_path, line_number, len(line), code_region.end_column)
            end_column += code_region.end_column
            break
        end_column += len(line)

    line = "".join(code_lines)
    start_column = code_region.start_column - 1

    return CodeReport(code_file_path, code_region, line[start_column:end_column])


# Check if a string starts with a white space character
def starts_with_space(input_string) -> bool:
    """
    Checks if a string starts with a white space character.

    Args:
        input_string (str): The input string to check.

    Returns:
        bool: True if the input string starts with a white space character, otherwise False.
    """
    return input_string and input_string[0].isspace()


def throw_invalid_line_length_exception(code_file_path: str, line_number: int, line_length: int, end_column: int):
    """
    Raises an exception for an invalid line length.

    Args:
        code_file_path (str): The path to the code file.
        line_number (int): The line number.
        line_length (int): The length of the line.
        end_column (int): The end column position.
    """
    raise InvalidLineException(f"Invalid line length. "
                               f"File: {code_file_path}, "
                               f"line number: {line_number}, "
                               f"line length: {line_length}, "
                               f"end column: {end_column}")


def throw_invalid_number_of_lines_exception(code_file_path: str, file_lines: int, end_line: int):
    """
    Raises an exception for an invalid number of lines.

    Args:
        code_file_path (str): The path to the code file.
        file_lines (int): The number of lines in the file.
        end_line (int): The end line position.
    """
    raise InvalidLineException(f"Invalid number of lines. "
                               f"File: {code_file_path}, "
                               f"file lines: {file_lines}, "
                               f"line end: {end_line}")
