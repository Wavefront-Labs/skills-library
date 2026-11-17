---
id: computing-software.web-development.hugo.hugo-modules-basics
name: hugo-modules-basics
category: computing-software
field: web-development
product: hugo
tags: [hugo-mod, go-mod, module-imports, vendoring, module-workspace]
level: practitioner
status: docs-checked
description: "Use Hugo Modules: hugo mod init, imports and precedence, get -u updates, tidy, vendor, graph, clean and workspaces for local development."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/hugo-modules/use-modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: install Git and Go.

Initialize: `hugo mod init github.com/user/project` creates `go.mod`. The name is a unique identifier; `my-project` also works.

Import: add `[[module.imports]]` entries with a `path` under `[module]` (the docs example mixes a bare name, an absolute directory and a remote repository path).

- Precedence is top-down: if two modules define the same shortcode, the first listed wins.
- Data files and translation tables with the same path are deeply merged, top-down.
- Imported modules mount their component directories automatically.
- Building downloads and caches modules and writes `go.sum`.

Commands:

- `hugo mod get -u` updates all; `hugo mod get -u github.com/user/shortcodes-c` one; add `@v0.42.0` to pin a version; `hugo mod get -u ./...` recurses.
- `hugo mod tidy` removes unused `go.mod` and `go.sum` entries.
- `hugo mod vendor` copies imports to `_vendor`, used by later builds. Modules in `themes` are not vendored. To customize a vendored file, add the same relative path in the project root. Delete `_vendor` to undo.
- `hugo mod graph` prints dependencies, showing replacements and `DISABLED` modules.
- `hugo mod clean` clears the current project's module cache; `--all` clears all projects.

Local development: use a `replace` directive in `go.mod`, the `replacements` config, or a workspace: create a `.work` file, set `workspace` or `HUGO_MODULE_WORKSPACE`, then run `HUGO_MODULE_WORKSPACE=hugo.work hugo server --ignoreVendorPaths "**"`.

## Checked

2026-11-04: prerequisites, hugo mod init, import precedence and merge, get/tidy/vendor/graph/clean commands and flags, replace directive, workspace and HUGO_MODULE_WORKSPACE, and automatic mounts confirmed against the Hugo docs Use modules page. Reworded the path description to what the example shows.

Method: documentation only; no commands were run.
