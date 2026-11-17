---
id: computing-software.software-engineering.pnpm.recursive-commands
name: recursive-commands
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-recursive, workspace-concurrency, no-bail, no-sort, reverse-order, topological-order, workspace-root-flag]
level: practitioner
status: docs-checked
description: "Run pnpm commands across a workspace with -r: which commands include the root, topological ordering, --workspace-concurrency, --no-bail, --no-sort, --reverse and --parallel."
sources:
  - https://pnpm.io/cli/recursive
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`-r` (aliases `m`, `multi`, `recursive`) runs a command in every workspace project.

- Includes the root: `install`, `list`, `outdated`, `publish`, `pack`, `rebuild`, `remove`, `unlink`, `update`, `why`.
- Excludes the root: `exec`, `run`, `test`, `add`. Set `includeWorkspaceRoot: true` to include it.
- Recursive `run`, `exec`, `test` execute in topological order (dependencies first). `--no-sort` drops graph ordering; `--parallel` starts tasks without waiting for dependencies.

Options:
- `--workspace-concurrency <n>` (setting `workspaceConcurrency`): default the smaller of 4 and available CPU cores; `Infinity` for unlimited; `0` or less means cores minus its absolute value, at least 1. In a container with a CPU quota the quota counts as the cores, fractions rounded down to at least 1.
- `--[no-]bail` (default true): stop on first error and kill running tasks (SIGTERM on Unix, SIGKILL after two seconds; ended at once on Windows). `--no-bail` is accepted only by `run`, `exec`, `test`, `start`, `stop`, `rebuild`, `install-test` and the script shorthand; tasks depending on a failure are skipped, the exit code is still non-zero.
- `--reverse`: reverse dependency edges, e.g. `pnpm -r --reverse run clean`.
- `-w` / `--workspace-root`, `--filter`, `--filter-prod`, `--resume-from`, `--stream`, `--aggregate-output`, `--report-summary`.

## Checked

2026-11-04. Confirmed the include and exclude root lists, topological ordering, --workspace-concurrency, --no-bail, --reverse and the remaining option list against pnpm.io/cli/recursive. Removed the unsourced claim that --parallel implies no sort, and the closing Check line.

Method: documentation only; no commands were run.
