---
id: computing-software.web-development.bun.workspace-filter
name: workspace-filter
category: computing-software
field: web-development
product: bun
tags: [bun-filter, workspace-scripts, dependency-order, parallel-scripts]
level: practitioner
status: docs-checked
description: "Select workspace packages with --filter patterns (names, paths, dependency graph forms) and run scripts across them in order, in parallel, or sequentially."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/filter.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Patterns:
- `name` glob on the `name` field (`@acme/*`); matches the full name, `*` does not cross `/`.
- `./packages/*` workspace directories (`./packages` alone selects nothing; `./` is the root).
- `foo...` foo plus dependencies; `foo^...` dependencies only; `...foo` foo plus dependents; `...^foo` dependents only.
- `!` prefix excludes (put it first: `!...foo`).

```bash
bun install --filter '!pkg-c'
bun --filter '*' dev                  # run script everywhere
bun --filter 'web...' build           # web and its deps, in dependency order
bun --filter '...^ui' test            # packages that depend on ui
bun run --parallel --filter '*' "build:*"
bun run --sequential --workspaces build
bun run --filter foo myscript          # run from a package in the same workspace
```

Gotchas:
- For package-manager commands put the flag after the subcommand (`bun install --filter api`); `bun --filter <pattern> <word>` runs `<word>` as a script.
- Positive patterns union; `!` patterns subtract. `install` and `outdated` default to all packages.
- Zero matches is a warning, but an error for `add`, `remove`, `update`, `prune`, `pm licenses`.
- `--no-exit-on-error` keeps others running with `--parallel`. Dependents start only after dependencies finish.

## Checked

2026-11-04. Confirmed against bun docs pm/filter.mdx: pattern forms and dependency-relation table, ./ root selector, exclusion order, union and subtraction, zero-match warning versus error, parallel and sequential flags, --no-exit-on-error, dependency ordering. Replaced an --if-present example whose placement the page does not show.

Method: documentation only; no commands were run.
