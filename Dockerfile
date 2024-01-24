FROM python:3.10-slim-buster

WORKDIR /app/

COPY /src ./src

COPY requirements.txt .

# COPY pyproject.toml .

RUN pip install -r /app/requirements.txt

# RUN pip install pdm

# RUN pdm install

EXPOSE 8889

EXPOSE 5678