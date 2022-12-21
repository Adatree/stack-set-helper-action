FROM python:3.10.7

# Install Poetry and update the package list
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry self update

# Set the working directory to the project root
WORKDIR /app

# Copy the project files
COPY . .

# Install project dependencies
RUN poetry install --no-dev

# Set the default command to run the project
ENTRYPOINT ["/entrypoint.sh"]
