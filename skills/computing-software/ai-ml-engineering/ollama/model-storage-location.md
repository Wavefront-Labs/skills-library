---
id: computing-software.ai-ml-engineering.ollama.model-storage-location
name: model-storage-location
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [ollama-models, model-directory, storage, chown]
level: practitioner
status: docs-checked
description: "Find where models are stored on macOS, Linux and Windows and move them with OLLAMA_MODELS and correct ownership."
sources:
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/windows.md
  - https://docs.ollama.com/macos.md
  - https://docs.ollama.com/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: relocate model storage to a bigger disk.

Default locations from the FAQ:

- macOS: `~/.ollama/models`
- Linux (service install): `/usr/share/ollama/.ollama/models`
- Windows: the `.ollama\models` folder in your user profile

The macOS page notes models can be tens to hundreds of GB, so a small home directory may not be enough. Override with `OLLAMA_MODELS`:

```
OLLAMA_MODELS=/path/to/models
```

On Linux the `ollama` user that runs the service must be able to read and write the new directory. The FAQ's fix is:

```
sudo chown -R ollama:ollama /path/to/models
```

Set the variable in the service with `systemctl edit ollama.service` (an `Environment="OLLAMA_MODELS=..."` line under `[Service]`), then run `systemctl daemon-reload` and `systemctl restart ollama`. On macOS use `launchctl setenv` and restart the app.

Windows: the install needs at least 4GB for the binary, plus space for models. Install elsewhere with `OllamaSetup.exe /DIR="<install directory>"`, and set `OLLAMA_MODELS` as a user environment variable (Settings or Control Panel, "Edit environment variables for your account") to put models on another drive; quit and relaunch the tray app afterwards. If you changed the model location, the uninstaller will not remove downloaded models.

Public key for pushing models: `id_ed25519.pub` in `~/.ollama` on macOS and `/usr/share/ollama/.ollama` on Linux. macOS logs are in `~/.ollama/logs`.

In Docker, the `-v ollama:/root/.ollama` volume holds the models.

## Checked

2026-11-08. Default paths, `OLLAMA_MODELS`, the `chown` note, key locations and per-OS variable setting against the FAQ (docs.ollama.com/faq); the 4GB requirement, `/DIR`, user-variable steps and uninstall note against the Windows page; tens-to-hundreds-of-GB note and `~/.ollama/logs` against the macOS page; the Docker volume against the Docker page. Corrected the `/DIR` example path (the page passes a directory path to the flag) and the Windows default path wording. Nothing else removed.

Method: documentation only; no commands were run.
