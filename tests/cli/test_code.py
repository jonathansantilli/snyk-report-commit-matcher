import json
import unittest
from unittest.mock import patch, Mock
from report import SarifReport, CodeRegion
from cli import (
    process_source_code,
    read_code_snippet,
    read_single_line_code_snippet,
    read_multiple_line_code_snippet,
    starts_with_space,
    InvalidLineException,
    InvalidContentException,
)


class TestCliCode(unittest.TestCase):

    def setUp(self):
        self.project_dir = 'tests/fixtures/project'
        self.code_file_path = 'tests/fixtures/snyk_report.json'
        self.sarif_report = Mock()
        self.code_region = Mock()
        self.code_region.start_line = 1
        self.code_region.end_line = 1
        self.code_region.start_column = 1
        self.code_region.end_column = 2

    def test_process_source_code(self):
        expected_number_of_files = 5
        with open(self.code_file_path, 'r') as json_file:
            report_data = json.load(json_file)
            sarif_report = SarifReport(report_data)

        code_reports = process_source_code(self.project_dir, sarif_report)

        self.assertEqual(len(code_reports), expected_number_of_files)
        self.assertEqual(code_reports[0].line_content, 'ServletUtil.establishSession(')
        self.assertEqual(code_reports[1].line_content, 'ServletUtil.establishSession(')
        self.assertEqual(code_reports[2].line_content, 'password.equals(')
        self.assertEqual(code_reports[3].line_content, 'password = request.getParameter("password");')
        self.assertEqual(code_reports[4].line_content, 'password.equals(')

    def test_process_source_code_invalid_content_in_location(self):
        with open('tests/fixtures/snyk_report_invalid_content_in_location.json', 'r') as json_file:
            report_data = json.load(json_file)
            sarif_report = SarifReport(report_data)

        with self.assertRaises(InvalidContentException):
            process_source_code(self.project_dir, sarif_report)

    def test_process_source_code_invalid_content_in_code_fow(self):
        with open('tests/fixtures/snyk_report_invalid_line_in_code_flow.json', 'r') as json_file:
            report_data = json.load(json_file)
            sarif_report = SarifReport(report_data)

        with self.assertRaises(InvalidContentException):
            process_source_code(self.project_dir, sarif_report)

    @patch('cli.code.read_multiple_line_code_snippet')
    @patch('cli.code.read_single_line_code_snippet')
    def test_read_code_snippet_single_line(self, mock_single_lines, mock_multiple_lines):
        code_region = CodeRegion({
                            'startLine': 10,
                            'endLine': 10,
                            'startColumn': 10,
                            'endColumn': 20
                    })

        read_code_snippet(self.code_file_path, code_region)

        mock_single_lines.assert_called()
        mock_multiple_lines.assert_not_called()

    def test_read_single_line_code_snippet(self):
        file_path = 'tests/fixtures/project/src/com/ibm/security/appscan/altoromutual/listener/StartupListener.java'
        code_region = CodeRegion({
            'startLine': 13,
            'endLine': 13,
            'startColumn': 17,
            'endColumn': 35
        })

        code_report = read_single_line_code_snippet(file_path, code_region)

        self.assertEqual(code_report.line_content, 'contextInitialized(')

    def test_read_single_line_code_snippet_throw_invalid_number_of_lines_exception(self):
        file_path = 'tests/fixtures/project/src/com/ibm/security/appscan/altoromutual/listener/StartupListener.java'
        code_region = CodeRegion({
            'startLine': 1000,
            'endLine': 1000,
            'startColumn': 17,
            'endColumn': 35
        })

        with self.assertRaises(InvalidLineException):
            read_single_line_code_snippet(file_path, code_region)

    def test_read_single_line_code_snippet_throw_invalid_line_length_exception(self):
        file_path = 'tests/fixtures/project/src/com/ibm/security/appscan/altoromutual/listener/StartupListener.java'
        code_region = CodeRegion({
            'startLine': 13,
            'endLine': 13,
            'startColumn': 1000,
            'endColumn': 1100
        })

        with self.assertRaises(InvalidLineException):
            read_single_line_code_snippet(file_path, code_region)

    def test_read_multiple_line_code_snippet(self):
        expected_lines = 'contextInitialized(ServletContextEvent sce) {' \
                         '\n        try {\n            ' \
                         'ServletUtil.initializeAppProperties(sce.getServletContext());\n'
        file_path = 'tests/fixtures/project/src/com/ibm/security/appscan/altoromutual/listener/StartupListener.java'
        code_region = CodeRegion({
            'startLine': 13,
            'endLine': 15,
            'startColumn': 17,
            'endColumn': 74
        })

        code_report = read_multiple_line_code_snippet(file_path, code_region)

        self.assertEqual(code_report.line_content, expected_lines)

    def test_read_multiple_line_code_snippet_throw_invalid_number_of_lines_exception(self):
        file_path = 'tests/fixtures/project/src/com/ibm/security/appscan/altoromutual/listener/StartupListener.java'
        code_region = CodeRegion({
            'startLine': 1000,
            'endLine': 1100,
            'startColumn': 17,
            'endColumn': 74
        })

        with self.assertRaises(InvalidLineException):
            read_multiple_line_code_snippet(file_path, code_region)

    def test_read_multiple_line_code_snippet_throw_invalid_line_length_exception(self):
        file_path = 'tests/fixtures/project/src/com/ibm/security/appscan/altoromutual/listener/StartupListener.java'
        code_region = CodeRegion({
            'startLine': 13,
            'endLine': 15,
            'startColumn': 1000,
            'endColumn': 1100
        })

        with self.assertRaises(InvalidLineException):
            read_multiple_line_code_snippet(file_path, code_region)

    def test_starts_with_space_true(self):
        self.assertTrue(starts_with_space(' starts with space'))

    def test_starts_with_space_false(self):
        self.assertFalse(starts_with_space('does not start with space'))
