---
id: computing-software.ai-ml-engineering.ollama.cli-model-management
name: cli-model-management
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [pull, rm, ls, signin, signout, cp, ollamapull]
level: intro
status: docs-checked
description: "Manage local models with ollama pull, ls, rm, create, cp, push and the signin/signout commands."
sources:
  - https://docs.ollama.com/cli.md
  - https://docs.ollama.com/import.md
  - https://docs.ollama.com/modelfile.md
  - https://docs.ollama.com/cloud.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know the housekeeping commands.

- `ollama pull <model>`: download a model, for example `ollama pull gemma4`.
- `ollama ls`: list installed models.
- `ollama rm <model>`: remove one.
- `ollama create <name> -f Modelfile`: build a model from a Modelfile (the Modelfile page shows `ollama create choose-a-model-name -f <location of the file>`).
- `ollama cp <source> <destination>`: copy a model under a new name; the sharing flow uses `ollama cp mymodel myuser/mymodel`.
- `ollama push <myuser/model>`: publish to ollama.com after adding your public key to your account (import page).
- `ollama signin` and `ollama signout`: sign in to and out of Ollama (CLI page).
- `ollama show --modelfile <model>`: print the Modelfile of a model (Modelfile page).
- `ollama ps`: loaded models.
- `ollama stop <model>`: stop a running model.
- `ollama serve`: start the server; `ollama serve --help` lists the environment variables it can read.

Names are `model:tag`. Cloud models are named differently in the app or CLI (`gemma4:cloud`) than in API requests to ollama.com (`gemma4:31b`), per the cloud page.

HTTP endpoints for the same jobs (from the API reference pages): `POST /api/pull`, `GET /api/tags`, `DELETE /api/delete`, `POST /api/create`, `POST /api/copy`, `POST /api/push`, `GET /api/ps` and `POST /api/show`.

## Checked

2026-11-08. The command list against the CLI page (docs.ollama.com/cli), `cp`/`push` flow against the import page, `show --modelfile` and `create -f` against the Modelfile page, cloud naming against the cloud page; endpoint paths and methods against each API reference page. Removed the claim that after sign-in local requests reach `-cloud` models such as `gpt-oss:120b-cloud` (not on the cited pages; the cloud page uses `:cloud`), and the gloss on signin/signout beyond the CLI page's headings. Reworded `stop` to the CLI page's "stop a running model".

Method: documentation only; no commands were run.
