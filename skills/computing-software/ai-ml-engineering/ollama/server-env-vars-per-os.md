---
id: computing-software.ai-ml-engineering.ollama.server-env-vars-per-os
name: server-env-vars-per-os
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [environment-variables, systemctl-edit, launchctl, windows-env, ollama-host]
level: intro
status: docs-checked
description: "Set Ollama server environment variables on macOS with launchctl, Linux with systemctl edit and Windows user variables."
sources:
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/linux.md
  - https://docs.ollama.com/windows.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make a setting survive restarts.

Variables must be set where the server process starts, not in your interactive shell.

macOS (app): `launchctl setenv OLLAMA_HOST "0.0.0.0:11434"`, then restart the Ollama application.

Linux (systemd):

1. `systemctl edit ollama.service`
2. Add lines under `[Service]`:

```
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

3. `systemctl daemon-reload` then `systemctl restart ollama`.

Windows: quit Ollama from the taskbar, open Settings (Windows 11) or Control Panel (Windows 10) and search for environment variables, edit or create the variable for your user account, then start Ollama again. The Windows page says Ollama needs no administrator rights and that `OLLAMA_MODELS` is a user variable.

Docker: pass `-e VAR=value` to `docker run`.

For several variables on Linux, add one `Environment=` line per variable under `[Service]`, for example `Environment="OLLAMA_KEEP_ALIVE=24h"` and `Environment="OLLAMA_MAX_QUEUE=512"`.

`ollama serve --help` lists the variables. Ones used across these skills: `OLLAMA_HOST` (default `127.0.0.1:11434`), `OLLAMA_ORIGINS`, `OLLAMA_MODELS`, `OLLAMA_KEEP_ALIVE`, `OLLAMA_MAX_QUEUE`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_NUM_PARALLEL`, `OLLAMA_CONTEXT_LENGTH`, `OLLAMA_FLASH_ATTENTION`, `OLLAMA_KV_CACHE_TYPE`, `OLLAMA_DEBUG`, `OLLAMA_NO_CLOUD` and `OLLAMA_VULKAN`.

## Checked

2026-11-03. launchctl, systemctl edit and Windows user-variable steps confirmed against the FAQ (docs.ollama.com/faq) and the Windows page; `OLLAMA_HOST` default, `ollama serve --help` (CLI page), `-e` for Docker and the listed variable names against the FAQ, GPU and Windows pages. Nothing removed.

Method: documentation only; no commands were run.
