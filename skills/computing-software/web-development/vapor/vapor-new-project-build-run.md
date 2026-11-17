---
id: computing-software.web-development.vapor.vapor-new-project-build-run
name: vapor-new-project-build-run
category: computing-software
field: web-development
product: vapor
tags: [vapor, vapor-new, vapor-run, hello-world, swift-run, xcode, working-directory, toolbox]
level: intro
status: docs-checked
description: "Create a Vapor project with vapor new, run it via Xcode or swift run, and set the Xcode working directory so .env and Public are found."
sources:
  - https://docs.vapor.codes/getting-started/hello-world/
  - https://docs.vapor.codes/getting-started/xcode/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: scaffold, run and visit a first Vapor app.

## Create
```sh
vapor new hello -n
cd hello
```
`-n` answers no to all questions for a bare-bones template. The Toolbox template requires Swift 6.0 or later. You can instead clone https://github.com/vapor/template-bare. The template uses async/await by default; if you cannot update to macOS 12 or need EventLoopFutures, use `--branch macos10-15`.

## Run
- Xcode: `open Package.swift`; wait for SPM dependency resolution (slow the first time) and for schemes to appear; pick the project scheme and a run target (likely "My Mac"); press Play. The console shows `[ INFO ] Server starting on http://127.0.0.1:8080`.
- Linux or any editor (Vim, VSCode; an official "Vapor for VS Code" extension exists): `swift run`. First run fetches and resolves dependencies, then prints the same server-starting line.

Visit http://localhost:8080/hello or http://127.0.0.1:8080; the page shows `Hello, world!`.

## Xcode custom working directory
By default Xcode runs from the DerivedData folder, not the folder holding Package.swift, so Vapor cannot find `.env` or `Public`. The symptom is this warning:
```
[ WARNING ] No custom working directory set for this scheme, using /path/to/DerivedData/project-abcdef/Build/
```
Fix: click the scheme selector by Play/Stop, choose Edit Scheme..., select the App action and the Options tab, tick "Use custom working directory" and enter the project root path. Get it by running `pwd` in a terminal opened in the project folder.

## Checked
Read the whole Hello, world and Xcode pages (vapor/docs, docs/4.0/getting-started/hello-world.md and xcode.md, sources of the cited pages) on 2026-11-08. Confirmed the `vapor new hello -n` command and flag meaning, Swift 6.0 template requirement, template-bare repository, `--branch macos10-15` note, both run paths and console line, the localhost page, and the whole custom working directory procedure and warning text. No claims removed.
Method: docs-only read of cited pages, 2026-11-08
