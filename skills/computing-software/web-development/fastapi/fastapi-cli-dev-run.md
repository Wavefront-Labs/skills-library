---
id: computing-software.web-development.fastapi.fastapi-cli-dev-run
name: fastapi-cli-dev-run
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, cli, fastapi-dev, fastapi-run, entrypoint, pyproject, auto-reload]
level: intro
status: docs-checked
description: "Use the fastapi command: fastapi dev versus fastapi run defaults, setting the app entrypoint in pyproject.toml, and the FASTAPI_ENV variable."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/fastapi-cli.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FastAPI CLI

It ships with `fastapi[standard]` and uses Uvicorn internally.

## Commands
- `fastapi dev`: development mode. Auto-reload on (resource-intensive, less stable), listens on `127.0.0.1`. It sets `FASTAPI_ENV=development` before importing the app and keeps an existing value (e.g. `staging`).
- `fastapi run`: production mode. Auto-reload off, listens on `0.0.0.0` (reachable by anyone who can reach the machine), normally behind a termination proxy for HTTPS. It leaves `FASTAPI_ENV` unchanged, so set it yourself if the app must detect production. Conventional values: `development`, `production`.

## Finding the app
- It auto-detects an object `app` in `main.py` (or a couple of variants).
- Explicit and recommended: `pyproject.toml` with `[tool.fastapi]` and `entrypoint = "main:app"` (or `"backend.main:app"` for `backend/main.py`), equal to `from backend.main import app`.
- Alternatives: pass a path (`fastapi dev main.py`) or `--entrypoint main:app` every time. Other tools (VS Code extension, FastAPI Cloud) may not find the app that way.

## Verify
Run `fastapi dev` and open `http://127.0.0.1:8000/docs`.

## Checked

Read the full fastapi-cli.md source page. Confirmed fastapi dev (auto-reload, 127.0.0.1, FASTAPI_ENV set to development unless already set), fastapi run (no reload, 0.0.0.0, FASTAPI_ENV unchanged, termination proxy for HTTPS), the pyproject.toml [tool.fastapi] entrypoint examples, the path and --entrypoint alternatives, and the editor and FastAPI Cloud caveat. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
