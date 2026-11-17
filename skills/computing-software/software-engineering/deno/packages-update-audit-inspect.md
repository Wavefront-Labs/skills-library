---
id: computing-software.software-engineering.deno.packages-update-audit-inspect
name: packages-update-audit-inspect
category: computing-software
field: software-engineering
product: deno
tags: [packages, outdated, update, why, info, audit, vulnerabilities]
level: practitioner
status: docs-checked
description: "Inspect and maintain dependencies: deno outdated, update (--latest), why, info, and deno audit with --level, --fix and --socket."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
See what is behind, then update:

```sh
deno outdated          # display what's behind, without changing anything
deno update            # update to the latest semver-compatible versions
deno update --latest   # ignore semver ranges and go to the newest releases
```

Find out where a package comes from; `deno why` prints every dependency path leading to it:

```sh
deno why npm:kleur
```

`deno info` shows a module's full dependency graph, including sizes and cache locations, for your entry point or any specifier:

```sh
deno info main.ts
deno info jsr:@std/http
```

`deno audit` checks installed dependencies against vulnerability databases:

```sh
deno audit                 # report known vulnerabilities
deno audit --level=high    # only high and critical severity
deno audit --fix           # upgrade affected packages automatically
deno audit --socket        # check against the socket.dev database
```

Auditing is one part of keeping the tree safe over time; see the supply chain guidance for minimum dependency age, lockfile discipline and a CI baseline.

## Checked

2026-11-04. Confirmed against the Deno Dependency management page: `deno outdated`, `deno update` and `--latest`, `deno why`, `deno info`, `deno audit` with `--level=high`, `--fix` and `--socket`. Nothing removed.

Method: documentation only; no commands were run.
