---
id: computing-software.software-engineering.wails.dev-mode
name: dev-mode
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, dev-server, live-reload, cli]
level: practitioner
status: docs-checked
description: "Run a Wails app in live development mode with wails dev: rebuilds, asset reload, browser access at localhost:34115 and the main flags."
sources: [https://wails.io/docs/gettingstarted/development, https://wails.io/docs/reference/cli]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Develop with wails dev

Goal: iterate quickly with automatic rebuild and reload.

## Method

Run `wails dev` from the project directory. It:
- updates go.mod to the CLI's Wails version, compiles and runs the app;
- watches Go files and rebuilds on change;
- loads assets from disk and reloads (not rebuilds) on asset change, including connected browsers;
- serves the whole app over http at `http://localhost:34115`, so browser extensions work and you can call Go from the browser console;
- generates the JS module wrappers for Go methods (with JSDoc), TypeScript versions of structs, and a runtime wrapper with TS declarations;
- on macOS bundles a `.app` using `build/darwin/Info.dev.plist`.

Example: `wails dev -assetdir ./frontend/dist -wailsjsdir ./frontend/src -browser`

Common flags (all in the CLI reference): `-browser`, `-devserver host:port`, `-frontenddevserverurl url` (for Vite or other servers), `-noreload`, `-debounce`, `-reloaddirs`, `-extensions`, `-tags`, `-s` (skip frontend build), `-skipbindings`, `-loglevel`, `-race`, `-appargs`, `-save` (persist certain flags into wails.json).

## Gaps
The getting-started page marks the dev tutorial as coming soon.

## Related skills
- computing-software.software-engineering.wails.cli-dev-flags

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Developing your Application" (gettingstarted/development); CLI reference (reference/cli).

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
