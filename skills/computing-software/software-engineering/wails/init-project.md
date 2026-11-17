---
id: computing-software.software-engineering.wails.init-project
name: init-project
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, project-setup, templates, cli]
level: practitioner
status: docs-checked
description: "Generate a new Wails project with wails init for a chosen frontend template and understand the generated directory layout."
sources: [https://wails.io/docs/gettingstarted/firstproject, https://wails.io/docs/tutorials/helloworld, https://wails.io/docs/reference/cli]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a Wails project

Goal: scaffold a project and know what each file is for.

## Method

Run `wails init -n myproject -t <template>`. Templates: svelte, react, vue, preact, lit, vanilla; add the `-ts` suffix for TypeScript (for example `svelte-ts`). Default template is vanilla. `wails init -help` lists options; community templates exist too.

Layout:

```
.
├── build/ (appicon.png, darwin/, windows/)
├── frontend/
├── go.mod
├── go.sum
├── main.go
└── wails.json
```

- `main.go`: the main application. The Hello World tutorial also shows `app.go` for application code.
- `frontend/`: nothing Wails-specific; any frontend project.
- `build/`: used during builds; files can be edited to customise builds; deleted files are regenerated with defaults. `appicon.png` is the app icon; `darwin/` and `windows/` hold platform files.
- `wails.json`: project configuration.

Example from the CLI reference: `wails init -n test -d mytestproject -g -ide vscode -q` (project "test" in "mytestproject", git initialised, VS Code files, quiet).

## Related skills
- computing-software.software-engineering.wails.install-wails-cli
- computing-software.software-engineering.wails.cli-init-and-remote-templates
- computing-software.software-engineering.wails.build-production-binary

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Creating a Project" (gettingstarted/firstproject); "Hello World" tutorial; CLI reference (reference/cli).

Corrected or removed: Added the CLI reference to sources; the example init command comes from it.

Method: documentation only; no commands were run.
