---
id: computing-software.software-engineering.v-lang.v-new-init-create-project
name: v-new-init-create-project
category: computing-software
field: software-engineering
product: v-lang
tags: [v-new-init-create-project, v-mod-and-module-search, v init, v new, scaffold, project template, create project, v-lang]
level: intro
status: draft
description: "Create a new project skeleton with v init or v new, generating v.mod, main.v and a .gitignore."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scaffolding projects with v init and v new

Goal: bootstrap quickly.

- `v init` in an empty directory writes `v.mod`, `main.v`, `.gitignore`/`.gitattributes` (confirm file list).
- `v new myapp` creates the folder first; `v new --web myweb` and `--lib` templates exist in recent versions (confirm with `v help new`).
- Edit v.mod metadata, then `v run .`.
- Add tests as `*_test.v`; add CI by running `v test .` and `v fmt -verify .`.

Gotchas:
- `v new` names must be valid module names (lowercase, no dashes).
- `v init` fails if a v.mod already exists.

Verify: `v run .` prints the default hello output.
