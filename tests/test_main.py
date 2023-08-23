import unittest
from unittest.mock import Mock, patch
from argparse import Namespace
from main import validate_arguments, parse_arguments


class TestParseArguments(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args', return_value=Namespace(
        repo_url="https://github.com/example/repo",
        commit_hash="commit123",
        report_path="snyk_report.json",
        debug=True
    ))
    def test_parse_arguments_with_valid_args_and_debug(self, mock_parse_args):
        parsed_args = parse_arguments()

        # Check if the arguments were correctly parsed
        self.assertEqual(parsed_args.repo_url, "https://github.com/example/repo")
        self.assertEqual(parsed_args.commit_hash, "commit123")
        self.assertEqual(parsed_args.report_path, "snyk_report.json")
        self.assertTrue(parsed_args.debug)

    @patch('argparse.ArgumentParser.parse_args', return_value=Namespace(
        repo_url="https://github.com/another/repo",
        commit_hash="commit456",
        report_path="another_report.json",
        debug=False
    ))
    def test_parse_arguments_with_valid_args_and_no_debug(self, mock_parse_args):
        parsed_args = parse_arguments()

        # Check if the arguments were correctly parsed
        self.assertEqual(parsed_args.repo_url, "https://github.com/another/repo")
        self.assertEqual(parsed_args.commit_hash, "commit456")
        self.assertEqual(parsed_args.report_path, "another_report.json")
        self.assertFalse(parsed_args.debug)


class TestValidateArguments(unittest.TestCase):
    def test_valid_arguments(self):
        # Create a mock 'args' object with valid arguments
        args = Mock(report_path='tests/fixtures/snyk_report.json', repo_url='https://github.com/example/repo')

        # The function should not raise any exceptions with valid arguments
        validate_arguments(args)

    def test_invalid_report_path(self):
        # Create a mock 'args' object with an invalid report path
        args = Mock(report_path='non_existent_report.json', repo_url='https://github.com/example/repo')

        # The function should raise an Exception for an invalid report path
        with self.assertRaises(Exception) as context:
            validate_arguments(args)

        self.assertIn("does not exist", str(context.exception))

    def test_invalid_repo_url(self):
        # Create a mock 'args' object with an invalid repo URL
        args = Mock(report_path='tests/fixtures/snyk_report.json', repo_url='http://example.com/repo')

        # The function should raise an Exception for an invalid repo URL
        with self.assertRaises(Exception) as context:
            validate_arguments(args)

        self.assertIn("is not valid", str(context.exception))
