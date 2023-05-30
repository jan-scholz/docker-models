FROM python:3.11-slim-bullseye as base

ARG PIP_DISABLE_PIP_VERSION_CHECK=1


FROM base as builder

WORKDIR /install

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* .

RUN poetry export --format requirements.txt --output requirements.txt --without-hashes

RUN pip install --no-cache-dir --target=/install -r requirements.txt

RUN find . -name 'tests' -type d -prune -exec rm -rf {} +


FROM base

WORKDIR /code

COPY --from=builder /install /usr/local/lib/python3.11/site-packages

COPY ./app /code/app

RUN python -m compileall app

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log", "--log-level", "critical"]
