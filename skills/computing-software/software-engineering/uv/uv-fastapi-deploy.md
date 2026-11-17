---
id: computing-software.software-engineering.uv.uv-fastapi-deploy
name: uv-fastapi-deploy
category: computing-software
field: software-engineering
product: uv
tags: [uv, fastapi, deployment, docker, uv-init, no-package, dev-server, web-api]
level: practitioner
status: docs-checked
description: "Adopt uv in an existing FastAPI app with uv init --no-package, run the dev server with uv run fastapi dev, and containerise it with a Dockerfile."
sources: [https://docs.astral.sh/uv/guides/integration/fastapi/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uv with FastAPI

Goal: manage an existing FastAPI project with uv, run it, and deploy via Docker.

## Method

For an app laid out as `project/app/` (`main.py`, `dependencies.py`, `routers/`, `internal/`), run inside `project`:

```console
$ uv init --no-package
$ uv add fastapi --extra standard
```

`--no-package` creates a `pyproject.toml` for a flat, unpackaged project (no build system) and leaves the existing files in place. The result lists `dependencies = ["fastapi[standard]"]` in `[project]`.

Run the dev server:

```console
$ uv run fastapi dev
```

`uv run` resolves and locks dependencies (creating `uv.lock` beside `pyproject.toml`), creates a virtual environment and runs the command in it. The page's example app is tested at `http://127.0.0.1:8000/?token=jessica`.

### Docker

```dockerfile
FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]
```

```console
$ docker build -t fastapi-app .
$ docker run -p 8000:80 fastapi-app
```

The container serves on port 80, published as 8000 locally. For more on using uv with Docker, see the uv Docker guide.

## Verify

Open `http://127.0.0.1:8000/?token=jessica` after `docker run -p 8000:80 fastapi-app` (or after `uv run fastapi dev`); the page says this confirms the app runs correctly.

## Checked

2026-11-07. Every command, flag, setting, default and example was read against the full text of the cited uv documentation pages (guides/integration/fastapi). Removed or changed: dropped an unconfirmed list of what the Docker guide covers.

Method: documentation only; no commands were run.
