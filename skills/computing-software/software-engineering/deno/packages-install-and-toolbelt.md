---
id: computing-software.software-engineering.deno.packages-install-and-toolbelt
name: packages-install-and-toolbelt
category: computing-software
field: software-engineering
product: deno
tags: [packages, deno-install, deno-add, npm, jsr, dependency-management]
level: intro
status: docs-checked
description: "Use Deno as the package manager for npm and JSR: deno install and add, bare-name imports, and the dependency subcommand toolbelt."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deno is a package manager for npm and JSR, working with `deno.json`, `package.json` or both.

```sh
deno install                    # install declared dependencies
deno install express            # unprefixed names are npm packages
deno install jsr:@std/assert    # a JSR package
```

The dependency is recorded in the config file and imported by bare name:

```ts
import express from "express";
import { assertEquals } from "@std/assert";
```

Toolbelt:

| Command | Purpose |
| --- | --- |
| `deno install` | Install dependencies (or a tool with `-g`) |
| `deno add` / `deno remove` | Add/remove a dependency in the config file |
| `deno outdated` / `deno update` | List / update newer versions |
| `deno why` | Explain why a package is in the tree |
| `deno info` | Module dependency graph and cache details |
| `deno audit` | Check for known vulnerabilities |
| `deno approve-scripts` | Approve npm lifecycle scripts |
| `deno ci` | Clean, lockfile-strict install for CI |
| `deno publish` / `deno pack` | Publish to JSR / build an npm tarball |
| `deno uninstall` | Remove a global tool |
| `deno clean` | Remove the global module cache |

HTTPS imports work but suit single-file scripts; registries are recommended since HTTPS imports can drift between files and are not managed by `deno add`.

## Checked

2026-11-04. Confirmed against the Deno Dependency management page: install and add commands, bare-name imports, the toolbelt table, HTTPS import guidance. Nothing removed.

Method: documentation only; no commands were run.
