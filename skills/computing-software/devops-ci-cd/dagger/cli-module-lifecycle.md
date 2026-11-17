---
id: computing-software.devops-ci-cd.dagger.cli-module-lifecycle
name: cli-module-lifecycle
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, cli, dagger-init, dagger-develop, dagger-install, toolchain, modules]
level: practitioner
status: docs-checked
description: "Create and maintain a Dagger module with dagger init, develop, install, uninstall, update, config and the toolchain subcommands."
sources: [https://docs.dagger.io/0.21/reference/cli]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dagger CLI: module lifecycle commands

Goal: scaffold a module, wire its SDK and dependencies, and keep it current. Dagger 0.21 docs CLI reference.

## Method

- `dagger init [options] [path]` creates `dagger.json` at the path, making it a module root. Options: `--sdk <sdk>` (install an SDK now; or later with `develop`), `--name` (defaults to parent directory name), `--source <dir>` (SDK source dir, default module root), `--include <paths>` (extra paths needed to build the module, relative to the dir containing `dagger.json`), `--license <SPDX id>` (default Apache-2.0), `--blueprint <module>` (reference another module as blueprint, remote or local), `--with-self-calls` (experimental). Docs examples:

```
dagger init --blueprint=github.com/example/blueprint
dagger init --blueprint=../my/blueprints/simple-webapp
dagger init --sdk=go
```

- `dagger develop` is idempotent. It ensures the SDK is installed and configured, updates the target engine version, creates a starter implementation if none exists, and regenerates client bindings for the API and installed dependencies. Use it: to add an SDK to a module without one, on a fresh checkout for IDE autocomplete, after changing local dependencies, and after upgrading the engine. Options: `--sdk` (builtin go, python, typescript, or a module address), `--source`, `-r/--recursive` (into local dependencies), `--compat` (engine API version, default latest), `--license`, `--with-self-calls` / `--without-self-calls`.
- `dagger install <module>` adds a dependency, e.g. `dagger install github.com/shykes/daggerverse/hello@v0.3.0`; `-n/--name` overrides the dependency name.
- `dagger uninstall <module>` removes a dependency; the target module must be local (example: `dagger uninstall hello`).
- `dagger update [<DEPENDENCY>...]` updates all dependencies, or only those named by short name or full address.
- `dagger config [-m path] [--json]` prints module configuration (get or set).
- Toolchains: `dagger toolchain install <module> [-n name]` (example `github.com/dagger/dagger/toolchains/go`), `dagger toolchain list`, `dagger toolchain update [<toolchain>...]`, `dagger toolchain uninstall <toolchain>`.
- Cloud auth: `dagger login [org]` and `dagger logout`.

## Gotchas

- `dagger update` is documented for local modules.
- Related: computing-software.devops-ci-cd.dagger.cli-running-functions, computing-software.devops-ci-cd.dagger.lockfiles, computing-software.devops-ci-cd.dagger.ide-setup.

## Checked

2026-11-07

Read in full from the docs source: reference/cli/index.mdx (the CLI reference page, all sections). Confirmed every init, develop, install, uninstall, update, config, toolchain, login and logout option, default and example quoted in the skill. No corrections needed.

Method: documentation only; no commands were run.
