FROM python:3.12.6

# Install Poetry and update the package list
RUN pip3 install poetry

# Set working directory
WORKDIR /app

# Install AWS cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm "awscliv2.zip"

# Copy the project files
COPY ./stack_set_helper_action ./stack_set_helper_action
COPY README.md .
COPY poetry.lock .
COPY pyproject.toml .
COPY entrypoint.sh .

ENV PYTHONPATH=/app
ENV VIRTUAL_ENV=./venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m venv ./venv
RUN chmod +x "./venv/bin/activate"
RUN poetry install --without dev
RUN chmod +x "./entrypoint.sh"

# Set the default command to run the project
ENTRYPOINT ["/app/entrypoint.sh"]
