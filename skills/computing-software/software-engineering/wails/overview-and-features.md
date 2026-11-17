---
id: computing-software.software-engineering.wails.overview-and-features
name: overview-and-features
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, desktop-apps, overview]
level: practitioner
status: docs-checked
description: "Explain what Wails is, its feature set, and how it differs from Electron, to decide whether it fits a Go desktop app."
sources: [https://wails.io/docs/introduction]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wails overview and features

Goal: decide whether Wails suits a project and describe it accurately.

## Method

Wails lets you write desktop apps in Go with a web frontend. The docs position it as a lightweight, fast Electron alternative for Go.

Key points to check against requirements:
- Platforms: Windows, macOS and Linux.
- Built-in templates for Svelte, React, Preact, Vue, Lit and Vanilla JS (JavaScript and TypeScript variants of each).
- It does not embed a browser. It reuses the platform's native rendering engine (Microsoft WebView2, built on Chromium, on Windows), so the runtime stays small.
- Go methods are exposed to JavaScript by name, and Go structs used by those methods generate TypeScript models.
- No CGO or external DLLs required on Windows.
- Native menus, dialogs, theming and translucency, plus a runtime library for both Go and JavaScript (events, logging, dialogs and more).
- Live development mode built on Vite: Go changes trigger a rebuild and relaunch, asset changes trigger a reload, and the running app is also served over a webserver so any browser can connect.
- Production build compiles to a single executable with assets bundled; on Windows and macOS a native package can be produced. Packaging assets (icon, info.plist, manifest) live in the project and can be customised.
- Apps are documented as Apple and Microsoft Store compliant.

## Related skills
- computing-software.software-engineering.wails.architecture-overview
- computing-software.software-engineering.wails.install-wails-cli

## Checked

2026-11-07. Read the whole Introduction page (website/docs/introduction.mdx): the Features list (native menus/dialogs/theming/translucency, Windows/macOS/linux, templates for Svelte, React, Preact, Vue, Lit and Vanilla JS, Go-to-TypeScript models, no CGO or external DLLs on Windows, Vite live development, Store compliance), the Quick Start Templates (JavaScript and TypeScript for each), Native Elements (does not embed a browser; WebView2 built on Chromium on Windows), the interoperability, runtime library, live development (rebuilds, reloads, browser webserver) and production-binary sections. Every point in the skill matched. No claims were trimmed. The architecture-overview skill listed as related was not part of this check.

Method: documentation only; no commands were run.
