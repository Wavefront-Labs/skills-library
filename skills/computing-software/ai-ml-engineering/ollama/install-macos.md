---
id: computing-software.ai-ml-engineering.ollama.install-macos
name: install-macos
category: computing-software
field: ai-ml-engineering
product: ollama
tags: [macos, ollama-dmg, apple-silicon, uninstall, ollamadmg]
level: intro
status: docs-checked
description: "Install Ollama on macOS Sonoma 14 or later, know where its files live, and stop it starting at login."
sources:
  - https://docs.ollama.com/macos.md
  - https://docs.ollama.com/faq.md
  - https://docs.ollama.com/gpu.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set up Ollama on a Mac.

Requirement: macOS Sonoma (14) or later. Apple M-series Macs get CPU and GPU support (the GPU page says GPU acceleration on Apple devices uses the Metal API); x86 Macs are CPU only.

Install by mounting `ollama.dmg` and dragging Ollama to the system-wide Applications folder. On startup the app checks that the `ollama` CLI is in your PATH and, if not, asks permission to create a link in `/usr/local/bin`. To install elsewhere, put the app where you want it, make sure `Ollama.app/Contents/Resources/ollama` (or a symlink) is on your PATH, and decline the "Move to Applications?" prompt.

Files:

- `~/.ollama` holds models (`~/.ollama/models`) and configuration, including the public key `id_ed25519.pub` and `server.json` (FAQ).
- `~/.ollama/logs` holds `app.log` (GUI) and `server.log` (read it for startup errors).

Environment variables: use `launchctl setenv`, for example `launchctl setenv OLLAMA_HOST "0.0.0.0:11434"`, then restart the app.

Startup: Ollama registers as a login item. To disable it, open Settings, search for "Login Items", find the Ollama entry under Allow in the Background and switch it off (the FAQ also gives the Windows Task Manager route).

Uninstall (macOS page): `sudo rm -rf /Applications/Ollama.app`, `sudo rm /usr/local/bin/ollama`, remove its folders under `~/Library` (Application Support, Saved Application State, Caches, WebKit) and `rm -rf ~/.ollama`.

Docker on macOS: the FAQ says GPU acceleration is not available for Docker Desktop on macOS.

## Checked

2026-11-08. Requirements, dmg install, PATH link, alternative install location, `~/.ollama` and log files, uninstall list against the macOS page (docs.ollama.com/macos); `launchctl setenv`, login item, key and `server.json` locations and Docker limitation against the FAQ; Metal against the GPU page. Replaced "through Metal" attribution on the macOS page with the GPU page, and added `app.log` and the alternate install route. Nothing removed.

Method: documentation only; no commands were run.
