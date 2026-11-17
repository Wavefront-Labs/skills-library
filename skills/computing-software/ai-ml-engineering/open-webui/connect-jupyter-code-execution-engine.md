---
id: computing-software.ai-ml-engineering.open-webui.connect-jupyter-code-execution-engine
name: connect-jupyter-code-execution-engine
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [open-webui, integrations, jupyter, code-execution, code-interpreter]
level: practitioner
status: docs-checked
description: "Point Open WebUI code execution and the code interpreter at a Jupyter server, with the env vars, token and password auth, persistence behaviour and the both-engines gotcha."
sources:
  - https://docs.openwebui.com/tutorials/integrations/dev-tools/jupyter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Connect Jupyter as the code execution engine

Goal: run model code on a Jupyter server instead of the default Pyodide interpreter engine (community guide, written against 0.5.16).

## 1. Stack
```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:latest
    ports: ["3000:8080"]
    volumes: [open-webui:/app/backend/data]
    extra_hosts: [host.docker.internal:host-gateway]
  jupyter:
    image: jupyter/minimal-notebook:latest
    ports: ["8888:8888"]
    volumes: [jupyter_data:<jovyan-home>/work]
    environment: [JUPYTER_ENABLE_LAB=yes, JUPYTER_TOKEN=123456]
volumes: {open-webui: {}, jupyter_data: {}}
```
`extra_hosts` makes `host.docker.internal` resolve on Linux; inside the same compose project `http://jupyter:8888` also works.

## 2. Configure (Settings > Admin > Code Execution, or env)
| Variable | Value |
|---|---|
| `ENABLE_CODE_INTERPRETER` | True |
| `CODE_EXECUTION_ENGINE` | jupyter |
| `CODE_EXECUTION_JUPYTER_URL` | http://host.docker.internal:8888 |
| `CODE_EXECUTION_JUPYTER_AUTH` | token |
| `CODE_EXECUTION_JUPYTER_AUTH_TOKEN` | 123456 |
| `CODE_EXECUTION_JUPYTER_TIMEOUT` | 60 |
| `CODE_INTERPRETER_ENGINE` | jupyter |
| `CODE_INTERPRETER_JUPYTER_URL/AUTH/AUTH_TOKEN/TIMEOUT` | same values |

## Rules
- The `CODE_INTERPRETER_JUPYTER_*` vars default to their `CODE_EXECUTION_JUPYTER_*` twins, but `CODE_INTERPRETER_ENGINE` defaults to `pyodide`, so set both engine variables.
- `CODE_EXECUTION_JUPYTER_AUTH` accepts exactly `token` or `password`; anything else sends no credentials. Password mode logs in through Jupyter's `/login` form.
- These are persisted settings: env vars apply only on the first start against a fresh database; afterwards the saved Admin value wins unless `ENABLE_PERSISTENT_CONFIG=False`.
- Keep `ENABLE_ORJSON` True (default; read at startup, restart after changing) for faster output of large prints or images.

## Test
Enable the Code Execution button in chat and prompt for CSV files, matplotlib charts, or a `notebook.ipynb`; check them in the Jupyter file browser.

## Gotcha
Every execution starts a fresh kernel and deletes it afterwards, so variables never persist and only files written to disk survive. To keep output, ask the model to save it to Jupyter explicitly (two steps: create, then save).

## Checked
2026-11-04. Confirmed against the Open WebUI docs page tutorials/integrations/dev-tools/jupyter (read in full): compose stack, extra_hosts note, every env var and value in the table, the persisted-settings behaviour, token or password auth, the CODE_INTERPRETER_ENGINE pyodide default, ENABLE_ORJSON, the test prompts and the fresh-kernel-per-run note. Removed: the claims that Jupyter is a legacy engine and that the Pyodide /mnt/uploads mount and Files panel do not exist on Jupyter (neither on the page).
Method: documentation only; no commands were run.
