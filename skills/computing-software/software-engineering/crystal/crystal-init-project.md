---
id: computing-software.software-engineering.crystal.crystal-init-project
name: crystal-init-project
category: computing-software
field: software-engineering
product: crystal
tags: [crystal-init-project, getting-started, crystal-init, scaffold, project-layout, app, lib, crystal]
level: intro
status: docs-checked
description: "Use crystal init app or lib to create a project with src, spec, shard.yml, LICENSE, README, .gitignore and a git repository; --force and --skip-existing."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/man/crystal/README.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/tools/init.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scaffold a project with crystal init

Goal: start a conventional project.

- `crystal init (lib|app) <name> [<dir>]`. `crystal init app myapp` creates `myapp/.gitignore`, `.editorconfig`, `LICENSE`, `README.md`, `shard.yml`, `src/myapp.cr`, `spec/spec_helper.cr` and `spec/myapp_spec.cr`, and initialises an empty Git repository.
- `lib` is a reusable library; `app` is an application not intended to be a dependency. A library has no `shard.lock` in its repository and no build target in `shard.yml`, but has instructions for using it as a dependency.
- `-f` / `--force` overwrites existing files; `-s` / `--skip-existing` skips them (the two cannot be combined).
- The author name and email come from `git config` (`user.name`, `user.email`), and the GitHub name from `github.user`; edit `shard.yml` afterwards if needed.

Gotchas:
- Not every generated file is required for every project; customise them.

Verify: `ls myapp` shows the files above.

## Checked

2026-11-03. Confirmed against the Crystal compiler manual (`crystal init` synopsis, created files, library rules) and the init tool source (`--force`, `--skip-existing`, git config lookups, `lib|app` types).
Removed: the `module Myapp` / `VERSION` constant claim, "names with dashes become CamelCase", the `crystal init --help` note and the build/spec verify command (not verified).
Method: documentation only; no commands were run.
