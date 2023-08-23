import os
import shutil
import unittest
from unittest.mock import Mock, patch, call
from git.exc import GitCommandError, InvalidGitRepositoryError
from repository import (
    CommitNotValidException,
    RepoNotValidException,
    clone_github_repository,
    checkout_to_commit
)


class TestGitFunctions(unittest.TestCase):

    def setUp(self):
        self.repo_url = "https://github.com/example/repo.git"
        self.destination_dir = "test_repo"
        self.commit_hash = "abcd1234"

    def tearDown(self):
        if os.path.isdir(self.destination_dir):
            shutil.rmtree(self.destination_dir)

    @patch('repository.git.Repo')
    def test_clone_github_repository(self, mock_repo):
        # Test cloning a valid repository
        expected_calls = [call.clone_from(self.repo_url, self.destination_dir)]

        clone_github_repository(self.repo_url, self.destination_dir)

        mock_repo.assert_has_calls(expected_calls)

    @patch('repository.git.Repo.clone_from')
    def test_clone_github_repository_existing_directory(self, mock_clone_from):
        clone_github_repository(self.repo_url, 'tests/repository')

        mock_clone_from.assert_not_called()

    @patch('repository.git.Repo.clone_from')
    def test_clone_github_repository_fails(self, mock_clone):
        mock_clone.side_effect = GitCommandError("clone", "error")

        with self.assertRaises(RepoNotValidException):
            clone_github_repository(self.repo_url, self.destination_dir)

    @patch('repository.git.Repo.clone_from')
    def test_clone_github_repository_invalid_url(self, mock_clone):
        # Test cloning with an invalid repository URL
        mock_clone.side_effect = InvalidGitRepositoryError("clone", "error")

        with self.assertRaises(RepoNotValidException):
            clone_github_repository("invalid_url", self.destination_dir)

    @patch('repository.github.git')
    def test_checkout_to_commit(self, mock_git):
        expected_calls = [call.Repo(), call.Repo(self.destination_dir), call.Repo().git.checkout(self.commit_hash)]
        mock_git.Repo().return_value = Mock()

        checkout_to_commit(self.destination_dir, self.commit_hash)

        mock_git.assert_has_calls(expected_calls)

    @patch('repository.github.git')
    def test_checkout_to_commit_invalid_commit(self, mock_git):
        mock_git.Repo().return_value = Mock()
        mock_git.Repo().git.checkout.side_effect = GitCommandError("checkout", "error")

        with self.assertRaises(CommitNotValidException):
            checkout_to_commit(self.destination_dir, "invalid_commit_hash")
