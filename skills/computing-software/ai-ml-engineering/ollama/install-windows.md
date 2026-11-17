---
id: computing-software.ai-ml-engineering.ollama.install-windows
name: install-windows
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [windows, ollamasetup, standalone-zip, nssm, ollamasetupexe]
level: intro
status: docs-checked
description: "Install Ollama on Windows 10 22H2 or later, choose an install directory, or use the standalone zip as a service."
sources:
  - https://docs.ollama.com/windows.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: install on Windows without administrator rights.

Requirements from the page: Windows 10 22H2 or newer (home or pro), NVIDIA drivers 551.61 or newer for NVIDIA cards, and no administrator rights are needed. Ollama is installed in your user account, and the page notes at least 4GB of space for the binary, plus space for models.

Run `OllamaSetup.exe`. Choose the install location from the command line with:

```
OllamaSetup.exe /DIR="/path/to/ollama"
```

Move models with the `OLLAMA_MODELS` user environment variable (see the model storage skill).

Files and logs live under `%LOCALAPPDATA%\Ollama`: `server.log`, `app.log` and `upgrade.log`.

Standalone CLI: download `ollama-windows-amd64.zip` (the page also lists AMD ROCm and MLX zips) when you want the binary without the tray app. The page says it can be run as a service with NSSM. For AMD GPU support the page says to extract `ollama-windows-amd64-rocm.zip` into the same directory.

GPU notes: Vulkan is the fallback for RDNA2 cards; AMD defaults are covered in the AMD skill.

Call the API from PowerShell, as the page demonstrates, using `Invoke-WebRequest` with POST against `http://localhost:11434/api/generate` with a JSON body, then `ConvertFrom-json` on the content.

Troubleshooting: older Windows 10 versions (for example 21H1) have a terminal bug that shows strings like `←[?25h` instead of control characters.

## Checked

2026-11-03. Requirements, `/DIR`, `OLLAMA_MODELS`, log files, standalone zips and NSSM, RDNA2/Vulkan note and the terminal bug confirmed against the Windows page. Fixed the PowerShell example (the page uses `Invoke-WebRequest`, not `Invoke-RestMethod`).

Method: documentation only; no commands were run.
