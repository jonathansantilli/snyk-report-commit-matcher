import argparse

from argparse import Namespace

from repository import clone_github_repository, checkout_to_commit, CommitNotValidException, RepoNotValidException
from cli import process_source_code, InvalidLineException, InvalidContentException
from report import SarifReport
from utils import read_json_file, get_project_dir, file_exists


def parse_arguments() -> Namespace:
    """
    Parse command-line arguments.

    Returns:
        Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Check if a Snyk Code report matches a repository and commit hash.")
    parser.add_argument("repo_url", type=str, help="GitHub repository URL.")
    parser.add_argument("commit_hash", type=str, help="Git commit hash.")
    parser.add_argument("report_path", type=str, help="Snyk report utils path")
    parser.add_argument("--debug", action='store_true', required=False,
                        help="Print a verbose report of what the program is doing and any error found")

    return parser.parse_args()


def validate_arguments(args):
    """
    Validate the command-line arguments.

    Args:
        args (Namespace): Parsed command-line arguments.

    Raises:
        Exception: If any of the arguments are invalid.
    """
    if not file_exists(args.report_path):
        raise Exception(f"The provided Snyk report: '{args.report_path}' does not exist.")

    if not args.repo_url.startswith('https://github.com'):
        raise Exception(f"The provided GitHub repo: '{args.repo_url}' is not valid.")


def print_error(exception: Exception, debug: bool):
    """
    Print an error message if debugging is enabled.

    Args:
        exception (Exception): The exception to print.
        debug (bool): Whether debugging is enabled.
    """
    if debug:
        print(exception)


def main() -> bool:
    """
    Checks whether a Snyk Code report matches a specific GitHub repository and commit hash.

    The conditions to detect whether the report was created for this specific
    GitHub repository and specific commit are the following:

        - Files in the report are not found within the GitHub project.
        - The start or end line given by the report are not found on the code file.
        - The start column is an empty line or whitespace character.
        - Commit hash is invalid or is not found.
        - Project in GitHub is not found or invalid.

    This is a short example of the Snyk report file and the information this program needs to determine
    if the report was created for this specific GitHub repository and specific commit:

    {
      "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
      "version": "2.1.0",
      "runs": [
        {
          "tool": {...},
          "results": [
            {
              "ruleId": "java/WebCookieMissesCallToSetHttpOnly",
              "ruleIndex": 0,
              "level": "note",
              "message": {...},
              "locations": [
                {
                  "physicalLocation": {
                    "artifactLocation": {
                      "uri": "src/com/ibm/security/appscan/altoromutual/servlet/LoginHttpServlet.java",
                      "uriBaseId": "%SRCROOT%"
                    },
                    "region": {
                      "startLine": 94,
                      "endLine": 94,
                      "startColumn": 36,
                      "endColumn": 64
                    }
                  }
                }
              ],
              "fingerprints": {...},
              "codeFlows": [
                {
                  "threadFlows": [
                    {
                      "locations": [
                        {
                          "location": {
                            "id": 0,
                            "physicalLocation": {
                              "artifactLocation": {
                                "uri": "src/com/ibm/security/appscan/altoromutual/servlet/LoginHttpServlet.java",
                                "uriBaseId": "%SRCROOT%"
                              },
                              "region": {
                                "startLine": 94,
                                "endLine": 94,
                                "startColumn": 36,
                                "endColumn": 64
                              }
                            }
                          }
                        }
                      ]
                    }
                  ]
                }
              ],
              "properties": {...}
            },
            {
              "ruleId": "java/TimingAttack",
              "ruleIndex": 1,
              "level": "warning",
              "message": {...},
              "locations": [
                {
                  "physicalLocation": {
                    "artifactLocation": {
                      "uri": "src/com/ibm/security/appscan/altoromutual/servlet/AdminLoginServlet.java",
                      "uriBaseId": "%SRCROOT%"
                    },
                    "region": {
                      "startLine": 45,
                      "endLine": 45,
                      "startColumn": 21,
                      "endColumn": 36
                    }
                  }
                }
              ],
              "fingerprints": {...},
              "codeFlows": [
                {
                  "threadFlows": [
                    {
                      "locations": [
                        {
                          "location": {
                            "id": 0,
                            "physicalLocation": {
                              "artifactLocation": {
                                "uri": "src/com/ibm/security/appscan/altoromutual/servlet/AdminLoginServlet.java",
                                "uriBaseId": "%SRCROOT%"
                              },
                              "region": {
                                "startLine": 41,
                                "endLine": 41,
                                "startColumn": 16,
                                "endColumn": 59
                              }
                            }
                          }
                        },
                        {
                          "location": {
                            "id": 1,
                            "physicalLocation": {
                              "artifactLocation": {
                                "uri": "src/com/ibm/security/appscan/altoromutual/servlet/AdminLoginServlet.java",
                                "uriBaseId": "%SRCROOT%"
                              },
                              "region": {
                                "startLine": 45,
                                "endLine": 45,
                                "startColumn": 21,
                                "endColumn": 36
                              }
                            }
                          }
                        }
                      ]
                    }
                  ]
                }
              ],
              "properties": {...}
            }
          ],
          "properties": {...}
        }
      ]
    }

    Returns:
        bool: True if the program detected the report matches the repo and hash, False otherwise.
    """
    args = parse_arguments()
    try:
        validate_arguments(args)

        repo_directory = get_project_dir(args.repo_url)

        clone_github_repository(args.repo_url, repo_directory)

        checkout_to_commit(repo_directory, args.commit_hash)

        report_data = read_json_file(args.report_path)

        sarif_report = SarifReport(report_data)

        result = process_source_code(repo_directory, sarif_report)

        if args.debug:
            for r in result:
                print(r.to_string())

        # Return `true` if the program detected the report matches the repo and hash
        return True
    except InvalidLineException as e:
        print_error(e, args.debug)
    except InvalidContentException as e:
        print_error(e, args.debug)
    except CommitNotValidException as e:
        print_error(e, args.debug)
    except FileNotFoundError as e:
        print_error(e, args.debug)
    except RepoNotValidException as e:
        print_error(e, args.debug)
    except Exception as e:
        print_error(e, args.debug)

    # Return `false` if the program detected the report does not match the repo and hash
    return False


if __name__ == "__main__":
    print(main())
