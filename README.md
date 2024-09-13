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
* (optional) pre-commit for checking build pipeline
  ```bash
  pip install pre-commit
  ```

## References:
* https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation.html
