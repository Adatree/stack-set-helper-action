FROM python:3.10.7

# Install Poetry and update the package list
RUN pip3 install poetry

# Install AWS cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm "awscliv2.zip"

# Copy the project files
COPY . .
ENV VIRTUAL_ENV=./venv

RUN python3 -m venv ./venv && \
    chmod -x "./venv/bin/activate" && \
    poetry install --no-dev
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the default command to run the project
CMD ["/entrypoint.sh"]
