FROM python:3.12.0-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade wheel "poetry==2.2.1"

RUN poetry config virtualenvs.create false

COPY Project_telegram/pyproject.toml Project_telegram/poetry.lock ./

RUN poetry install

COPY Project_telegram .

CMD ["python", "main.py"]