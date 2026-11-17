---
id: computing-software.cloud-infrastructure-engineering.docker.docker-desktop-diagnostics-and-troubleshooting
name: docker-desktop-diagnostics-and-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-desktop, desktop-diagnostics, com-docker-diagnose, troubleshooting, wsl2, desktop-logs, factory-reset, docker-desktop-cli]
level: practitioner
status: docs-checked
description: "Diagnose a broken Docker Desktop: docker desktop diagnose, com.docker.diagnose gather, WSL2/Hyper-V/virtualisation failures, and the restart, clean-up and factory-reset ladder."
sources: ["https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/", "https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/", "https://docs.docker.com/desktop/features/desktop-cli/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Desktop diagnostics and troubleshooting

**Goal:** get from "Docker Desktop is starting..." forever, or "Cannot connect to the Docker
daemon", to a cause, without reinstalling as the first move.

## 1. Is it the app, the VM or the CLI context?
```bash
docker context ls                  # is the current context desktop-linux / default?
docker desktop status              # Desktop CLI: running or stopped
docker version                     # Server section missing = engine not reachable
```
A wrong context (left over from another runtime, a remote host or a `DOCKER_HOST` variable)
looks like a dead Desktop: `unset DOCKER_HOST; docker context use desktop-linux`.

## 2. Self-diagnose
Troubleshoot menu: **Get support** collects diagnostics, then **Upload to get a Diagnostic ID**.
From a terminal (useful when the Dashboard will not start) the documented command is:
```bash
docker desktop diagnose
```
It prints a diagnostics ID (your user ID plus a timestamp) and the path of the diagnostics
zip. Gathering can take several minutes; do not close Desktop meanwhile. The lower-level tool
does the same job when the Desktop CLI is unavailable:
```bash
# macOS
/Applications/Docker.app/Contents/MacOS/com.docker.diagnose gather -upload
# Windows (PowerShell), all-user installation
& "$env:ProgramFiles\Docker\Docker\resources\com.docker.diagnose.exe" gather -upload
# Linux
/opt/docker-desktop/bin/com.docker.diagnose gather -upload
```
Quote the diagnostics ID to Docker support (subscribers) or in a new issue on the
docker/desktop-feedback GitHub repository. `docker desktop logs` prints log entries.
Daemon logs are covered in the Engine docs ("Read the daemon logs").

## 3. Common causes on Windows
- `wsl -l -v` should list `docker-desktop` at version 2; the docs' own check is
  `wsl -d docker-desktop echo WSL 2 is working`.
- Error codes `HCS_E_HYPERV_NOT_INSTALLED` or `ERROR_NOT_SUPPORTED` (also from plain `wsl`
  commands) mean virtualisation is off in firmware or the Hyper-V / WSL 2 components are
  missing. WSL 2 needs *Virtual Machine Platform*, *Windows Subsystem for Linux*, firmware
  virtualisation and the hypervisor enabled at Windows startup; the Hyper-V backend needs
  Hyper-V installed. Some third-party software (Android emulators) disables Hyper-V.
- Anti-virus or endpoint "hardened" virtualisation modes that claim exclusive access to
  Hyper-V can stop Desktop and WSL starting.
- Network subnet clashes: Settings, Resources, Network lets you set a custom Docker subnet.
- "port already allocated": see the port-conflict skill.

## 4. Common cause on macOS
"Docker.app is damaged and can't be opened" comes from a non-atomic drag-and-drop install
while another tool (an IDE, a script) was calling the Docker CLI. Quit anything calling
Docker, move `/Applications/Docker.app` to the Trash, reinstall, and gather diagnostics if it
persists.

## 5. Escalating resets (least destructive first)
1. Troubleshoot, **Restart Docker Desktop** (`docker desktop restart`).
2. **Clean up data**: destroys all local containers and images, keeps settings.
3. **Reset to factory defaults**: resets every option to its initial state.
Back up named volumes first.

## Verify
```bash
docker run --rm hello-world
docker desktop status
```

## Checked
Date: 2026-10-26. Documentation: docker/docs repository main branch (last commit 2026-10-23),
pages for troubleshooting, troubleshooting topics and the Desktop CLI. Confirmed: `docker
desktop diagnose`, `com.docker.diagnose gather -upload` and its per-OS paths, the Troubleshoot
menu entries and the reset ladder, the CLI subcommand list (start, stop, restart, status,
logs, diagnose), the Windows virtualisation error codes and prerequisites, the macOS "damaged"
cause and fix. Removed as unconfirmed: the `check` subcommand, per-OS log folder table,
Desktop CLI version gate, the 192.168.65.0/24 subnet, `wsl --update` advice, the tar backup
one-liner.
Method: documentation only; no commands were run.
