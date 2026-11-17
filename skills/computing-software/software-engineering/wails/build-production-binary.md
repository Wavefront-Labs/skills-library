---
id: computing-software.software-engineering.wails.build-production-binary
name: build-production-binary
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, build, packaging, cli]
level: practitioner
status: docs-checked
description: "Compile a Wails project with wails build into build/bin, run the result per OS, and apply the Linux webkit2_41 tag when needed."
sources: [https://wails.io/docs/gettingstarted/building, https://wails.io/docs/tutorials/helloworld, https://wails.io/docs/reference/cli]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build a production binary

Goal: produce the distributable app.

## Method

From the project directory run `wails build`. The binary lands in `build/bin`.

On Linux distros lacking webkit2gtk-4.0 (such as Ubuntu 24.04): `wails build -tags webkit2_41`.

Tutorial output (Windows) shows stages: installing frontend dependencies, compiling frontend, generating bundle assets, compiling application, then `Built '.../build/bin/helloworld.exe'`. The header also lists settings such as App Type, Platforms, Compiler, Build Mode, Devtools, Skip Frontend, Compress, Package, LDFlags, Tags, Race Detector.

Running it:
- Windows: double-click `helloworld.exe`.
- macOS: Wails generates `helloworld.app`; double-click it.
- Linux: `./helloworld` from `build/bin`.

For all options see the build flags skill. For standard Go tooling instead of the CLI, the CLI reference points to the Manual Builds guide.

## Gotchas
- On macOS the bundle uses `Info.plist`, not `Info.dev.plist`.

## Related skills
- computing-software.software-engineering.wails.cli-build-flags
- computing-software.software-engineering.wails.init-project

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Compiling your Project" (gettingstarted/building); "Hello World" tutorial; CLI reference (reference/cli).

Corrected or removed: Added the CLI reference to sources, since the Info.plist and Manual Builds statements come from it.

Method: documentation only; no commands were run.
