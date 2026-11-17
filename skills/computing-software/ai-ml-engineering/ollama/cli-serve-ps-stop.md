---
id: computing-software.ai-ml-engineering.ollama.cli-serve-ps-stop
name: cli-serve-ps-stop
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [ollama-serve, ollama-ps, ollama-stop, unload, ollamaps]
level: intro
status: docs-checked
description: "Start the server with ollama serve, see loaded models and their processor split with ollama ps, and unload with ollama stop."
sources:
  - https://docs.ollama.com/cli.md
  - https://docs.ollama.com/context-length.md
  - https://docs.ollama.com/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: inspect and control what is in memory.

`ollama serve` starts the server on `127.0.0.1:11434` by default (`OLLAMA_HOST` changes it). `ollama serve --help` lists the environment variables, and settings pass as a prefix, for example:

```
OLLAMA_CONTEXT_LENGTH=64000 ollama serve
```

`ollama ps` lists loaded models. The context-length page says to check the allocation there: the PROCESSOR column shows how the model is split between GPU and CPU and the CONTEXT column shows the context in use.

`ollama stop <model>` unloads a model immediately. Without it, a model stays loaded for 5 minutes after the last request by default (`OLLAMA_KEEP_ALIVE` or the API `keep_alive` change that).

Preloading: `ollama run llama3.2 ""` loads a model without a prompt, per the FAQ.

On Linux the server normally runs as a systemd service named `ollama`, so read its logs with `journalctl -e -u ollama`.

## Checked

2026-11-03. `ollama serve`, `ps`, `stop`, `serve --help` against the CLI page; 5-minute default unload, preload and `ollama ps` columns against the FAQ (docs.ollama.com/faq) and the context-length page; `journalctl -e -u ollama` against the Linux page. Removed the `GET /api/ps` field list (the API page was not fetched).

Method: documentation only; no commands were run.
