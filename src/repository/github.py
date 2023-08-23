import git
from git.exc import GitCommandError, InvalidGitRepositoryError
from utils import dir_exists


class CommitNotValidException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RepoNotValidException(Exception):
    def __init__(self, message):
        super().__init__(message)


def clone_github_repository(repo_url, destination_dir):
    """
    Clone a GitHub repository to a destination directory if it doesn't already exist.

    Args:
        repo_url (str): The URL of the GitHub repository.
        destination_dir (str): The directory where the repository will be cloned.

    Raises:
        RepoNotValidException: If cloning or repository validation fails.
    """
    try:
        if not dir_exists(destination_dir):
            git.Repo.clone_from(repo_url, destination_dir)
    except GitCommandError as e:
        raise RepoNotValidException(f"Failed to clone repository: {e}")
    except InvalidGitRepositoryError as e:
        raise RepoNotValidException(f"'{destination_dir}' is not a valid Git repository: {e}")


def checkout_to_commit(repo_path, commit_hash):
    """
    Checkout to a specific commit in a Git repository.

    Args:
        repo_path (str): The path to the Git repository.
        commit_hash (str): The commit hash to check out.

    Raises:
        CommitNotValidException: If checking out to the commit fails.
    """
    try:
        repo = git.Repo(repo_path)
        repo.git.checkout(commit_hash)
    except GitCommandError as e:
        raise CommitNotValidException(f"Failed to checkout to commit: {commit_hash}\nError: {e}")