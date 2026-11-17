---
id: computing-software.software-engineering.wails.cli-generate-update-version
name: cli-generate-update-version
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, cli, bindings, maintenance]
level: practitioner
status: docs-checked
description: "Use wails generate module and template, wails update and wails version, plus wails doctor output, for maintenance tasks."
sources: [https://wails.io/docs/reference/cli]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wails generate, update, version, doctor

Goal: use the smaller CLI commands correctly. All commands run as `wails <command> <flags>`.

## Method

- `wails generate module`: manually regenerate the `wailsjs` directory. Flags: `-compiler` (default go), `-tags "extra tags"`.
- `wails generate template`: scaffold a template so it can be used by `wails init`. Flags: `-name` (mandatory), `-frontend "path"` (frontend project to include). See the Templates guide for details.
- `wails update`: updates the CLI. Flags: `-pre` (latest pre-release), `-version "version"` (specific version).
- `wails version`: prints the CLI version.
- `wails doctor`: diagnostics. The sample output lists system info (OS, Go version, platform, architecture), a dependency table (WebView2, npm, optional upx marked with an asterisk) and a Diagnosis line such as "Your system is ready for Wails development!".

Use `generate module` when you need bindings without running `wails dev`.

## Related skills
- computing-software.software-engineering.wails.install-wails-cli
- computing-software.software-engineering.wails.call-go-from-frontend

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: CLI reference (reference/cli).

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
