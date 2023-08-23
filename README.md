# Snyk Code Report Validator

The Snyk Code Report Validator is a CLI tool written in Python 3 that checks whether a Snyk Code report matches a specific GitHub repository and commit hash.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Tests](#tests)
- [Contributing](#contributing)

## Prerequisites

Before using this tool, ensure you have the following prerequisites installed:

- Python 3.x: [Python Downloads](https://www.python.org/downloads/)

## Installation

1. Clone this repository:

   ```shell
   git clone git@github.com:jonathansantilli/snyk-report-commit-matcher.git
   cd snyk-report-commit-matcher
   ```

2. Install the required dependencies:

  ```shell
  pip install -r requirements.txt
  ```

## Usage

The tool can be run from the command line as follows:

```shell
python src/main.py <repo_url> <commit_hash> <report_path> [--debug]
```

- <repo_url>: GitHub repository URL.
- <commit_hash>: Git commit hash.
- <report_path>: Path to the Snyk Code report JSON file.
- --debug (optional): Print verbose output for debugging.

The program will clone the GitHub repository into the `projects` folder just once.
(See the `get_project_dir` function in `src/utils/file.py`)

For instance, for the GitHub repo `https://github.com/in28minutes/spring-boot-examples`, the project
will be cloned in `projects/in28minutes/spring-boot-examples`.

If you want to clone it again, remove the whole `projects` folder or the specific one.

## Examples

Here are some example usages of the tool:

```shell
python src/main.py https://github.com/in28minutes/spring-boot-examples 62fd5519b7888077a38451f1759baeca5561199a report.json
# Output: true

python src/main.py https://github.com/in28minutes/spring-boot-examples 4813edb02c7b7c2f3cfbcc6330039686b2a5b416 report.json
# Output: false
```

## Tests

Run the following command to execute the tests:

```shell
PYTHONPATH=src pytest
```

## Contributing

Contributions are welcome! If you have any ideas or improvements, please submit a pull request.