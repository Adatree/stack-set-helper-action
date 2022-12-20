FROM python:3.10.7

# Install Poetry and update the package list
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 && \
    poetry self update

# Set the working directory to the project root
WORKDIR /app

# Copy the project files
COPY . .

# Install project dependencies
RUN poetry install --no-dev

# Set the default command to run the project
ENTRYPOINT ["python", "stack_set_helper_action/main.py"]
