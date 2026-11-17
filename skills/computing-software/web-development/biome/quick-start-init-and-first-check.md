---
id: computing-software.web-development.biome.quick-start-init-and-first-check
name: quick-start-init-and-first-check
category: computing-software
field: web-development
product: biome
tags: [biome, quick-start, biome-init, biome-json, check, write, schema, first-run]
level: intro
status: docs-checked
description: "Go from nothing to a first biome check: install, run biome init for biome.json with the JSON schema, then check and check --write."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/installation/quick-start.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three steps from a project without Biome to a first check.

1. **Install** with a package manager (`npm i -D -E @biomejs/biome`) or the standalone installer. `-E` pins the exact version.
2. **Create a configuration file.** Biome works without one, but `biome.json` lets you share settings with the team and the editor:

```sh
npx @biomejs/biome init
```

The generated file enables the formatter, the linter and assist actions with their recommended settings, and references the JSON Schema so editors can complete and document every option.

3. **Check the project** in one pass:

```sh
npx @biomejs/biome check
npx @biomejs/biome check --write
```

`check` lists every file that is not formatted and every diagnostic found. `--write` applies formatting, safe lint fixes and assist actions. Diagnostics that remain either have no fix or have a fix that is unsafe to apply automatically, so they need your attention.

**Next steps named by the docs:**
- Set up your editor for diagnostics as you type and format on save.
- Configure Biome to change formatter options, enable or disable rules and choose which files are processed.
- Integrate with VCS to reuse `.gitignore` and check only changed files.
- Add Biome to CI so code is checked before merging.

Verify: after `check --write`, a second `check` reports no formatting differences.

## Checked

2026-11-08. Read the Biome Quick start page in full. Confirmed the install, init and check steps, -E pinning, what check and --write do, and the next steps list. Removed the biome ci mention, which that page does not contain.

Method: documentation only; no commands were run.
