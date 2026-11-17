---
id: computing-software.software-engineering.wails.cli-dev-flags
name: cli-dev-flags
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, cli, dev-server, vite]
level: practitioner
status: docs-checked
description: "Tune wails dev with flags for asset directory, third-party dev servers like Vite, reload behaviour, dev server address and saving defaults."
sources: [https://wails.io/docs/reference/cli, https://wails.io/docs/guides/application-development]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wails dev flags

Goal: configure live development for your frontend setup.

## Method

Flags and defaults:
- `-assetdir path`: serve assets from this directory (default: wails.json value).
- `-frontenddevserverurl url`: use a third-party dev server such as Vite. `-viteservertimeout` (default 10 seconds) applies when the URL is `auto`.
- `-devserver host:port` (default `localhost:34115`), `-browser` opens it at startup.
- `-reloaddirs`, `-extensions` (default go), `-debounce` (default 100 ms), `-noreload`.
- `-wailsjsdir`: where generated JS modules go.
- `-appargs "args"`: shell-style args to the app.
- Build controls: `-compiler`, `-tags`, `-ldflags`, `-race`, `-s`, `-forcebuild`, `-skipbindings`, `-skipembedcreate`, `-nosyncgomod`.
- Output: `-loglevel` (Trace, Debug, Info, Warning, Error; default Debug), `-v`, `-nocolour`.
- `-save`: stores assetdir, reloaddirs, wailsjsdir, debounce, devserver, frontenddevserverurl and viteservertimeout into wails.json as defaults.

Example: `wails dev -assetdir ./frontend/dist -wailsjsdir ./frontend/src -browser` builds and runs, generates JS modules in ./frontend/src, watches ./frontend/dist and opens a browser.

For integration with existing framework scripts and external dev servers (for example Create React App), see the Application Development guide.

## Related skills
- computing-software.software-engineering.wails.dev-mode
- computing-software.software-engineering.wails.wails-json-config

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: CLI reference (reference/cli); "Application Development" guide.

Corrected or removed: Removed the "was not read" note and replaced it with a pointer to the Application Development guide, now read and added to sources.

Method: documentation only; no commands were run.
