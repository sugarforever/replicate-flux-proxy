# Replicate Flux API Proxy

This is a Replicate API proxy that mainly allows Dify users to integrate Flux into workflow.

## Get Started

### Install Poetry

```shell
curl -sSL https://install.python-poetry.org | python3 -
```

### Install Dependencies

```shell
poetry install
```

### Run

```shell
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```