# StackSetHelper Github Action

## Pre-requisites

* python version 3.12.6 or higher
* poetry - this is a python package manager
   * don't use homebrew, reference: https://python-poetry.org/docs/#installing-with-pipx
   * or https://python-poetry.org/docs/#installing-with-the-official-installer
* If you use zsh, make sure you add the following to the top of your `.zshrc`:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```
* pre-commit - for automatically fix linting errors
  ```bash
  pip install pre-commit
  ```

## Usage

For updating dependencies to latest:
```bash
poetry update <dependency>
```

For running tests locally:
```bash
poetry run pytest
```

For triaging `pre-commit` config issues:
```bash
pre-commit run --all-files
```

## References:
* https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html
