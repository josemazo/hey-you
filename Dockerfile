FROM python:3.7.3-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=0.12.16
ENV PATH=$PATH:/usr/src/app

# One liners for development purposes
RUN apt-get update
RUN apt-get install -y --no-install-recommends git build-essential
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config settings.virtualenvs.create false
RUN poetry completions bash > /etc/bash_completion.d/poetry.bash-completion
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi
RUN apt-get remove -y --purge git build-essential
RUN apt-get autoremove -y
RUN apt-get clean -y
RUN rm -rf /var/lib/apt/lists/*

COPY . .
