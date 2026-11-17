---
id: computing-software.ai-ml-engineering.ollama.troubleshooting-logs-and-debug
name: troubleshooting-logs-and-debug
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [logs, journalctl, ollama-debug, server-log]
level: intro
status: docs-checked
description: "Find server logs on macOS, Linux, Docker and Windows and turn on OLLAMA_DEBUG=1 for more detail."
sources:
  - https://docs.ollama.com/troubleshooting.md
  - https://docs.ollama.com/windows.md
  - https://docs.ollama.com/macos.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: capture useful diagnostics.

Log locations from the troubleshooting page:

- macOS: `cat ~/.ollama/logs/server.log`
- Linux (systemd): `journalctl -u ollama --no-pager --follow --pager-end`
- Docker: `docker logs <container-name>` (find the name with `docker ps`)
- Windows: `%LOCALAPPDATA%\Ollama` holds `server.log`, `app.log` (GUI app) and `upgrade.log`. Open the folder with `explorer %LOCALAPPDATA%\Ollama`.

When running `ollama serve` manually, the logs print to the terminal.

Enable debug logging with the environment variable:

```
OLLAMA_DEBUG=1 ollama serve
```

On Linux add it as an `Environment=` line with `systemctl edit ollama.service`. On Windows, first quit the running app from the tray menu, then in PowerShell run `$env:OLLAMA_DEBUG="1"` and `& "ollama app.exe"`.

Other Windows folders (via `explorer`): `%LOCALAPPDATA%\Programs\Ollama` for binaries, `%HOMEPATH%\.ollama` for models and configuration, and `%TEMP%` for temporary executables in `ollama*` directories. Older logs are `server-#.log`. A line `Ollama cloud disabled: true` confirms cloud features are off.

When filing an issue, attach the relevant log. Additional GPU diagnostics: `AMD_LOG_LEVEL=3` for ROCm and `CUDA_ERROR_LEVEL=50` for CUDA (see the GPU discovery skill).

## Checked

2026-11-03. Log locations for macOS, Linux, Docker and Windows, `OLLAMA_DEBUG=1`, Windows folders and PowerShell steps against the troubleshooting page (docs.ollama.com/troubleshooting) and the Windows page; `Ollama cloud disabled: true` against the FAQ (docs.ollama.com/faq); `AMD_LOG_LEVEL=3` and `CUDA_ERROR_LEVEL=50` against the troubleshooting page (docs.ollama.com/troubleshooting). Nothing removed.

Method: documentation only; no commands were run.
