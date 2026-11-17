---
id: computing-software.software-engineering.wails.install-wails-cli
name: install-wails-cli
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, installation, doctor, cli]
level: practitioner
status: docs-checked
description: "Install Go, Node and platform dependencies, install the Wails CLI with go install, and verify the setup with wails doctor."
sources: [https://wails.io/docs/gettingstarted/installation]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install Wails and check the system

Goal: get a working `wails` command and a clean `wails doctor`.

## Method

Supported platforms: Windows 10/11 AMD64/ARM64; macOS 10.15+ AMD64 for development (10.13+ release) and 11.0+ ARM64; Linux AMD64/ARM64.

1. Install Go 1.21+ (macOS 15+ needs Go 1.23.3+). Ensure `~/go/bin` is on PATH, restart the terminal, then check `go version` and `echo $PATH | grep go/bin`.
2. Install NPM (Node 15+, latest recommended). Check with `npm --version`.
3. Platform dependencies:
   - macOS: `xcode-select --install`.
   - Windows: the WebView2 runtime (some installs already have it; `wails doctor` checks).
   - Linux: gcc build tools plus libgtk3 and libwebkit. `wails doctor` shows distro-specific install commands. On distros without libwebkit2gtk-4.0-dev (for example Ubuntu 24.04), install `libwebkit2gtk-4.1-dev` and build with `-tags webkit2_41`.
4. Optional: UPX (compress binaries), NSIS (Windows installers).
5. Install the CLI: `go install github.com/wailsapp/wails/v2/cmd/wails@latest`
6. Run `wails doctor`; it reports missing dependencies and how to fix them.

## Gotchas
- Error like `pattern all:ides/*: no matching files found`: check Go is 1.18+ (`go version`).
- `wails` not found: the go/bin directory is usually missing from PATH; reopen the terminal after changing it. On Linux: `export PATH=$PATH:$(go env GOPATH)/bin` then source ~/.bashrc or ~/.zshrc.
- Windows 11: the docs suggest a Dev Drive for projects (they claim up to 30% faster builds).

## Related skills
- computing-software.software-engineering.wails.init-project

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Installation" (gettingstarted/installation).

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
