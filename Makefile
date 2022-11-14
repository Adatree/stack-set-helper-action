run-tests:
	pytest --log-cli-level=INFO tests

setup:
	-pre-commit clean
	pre-commit install
	poetry install
