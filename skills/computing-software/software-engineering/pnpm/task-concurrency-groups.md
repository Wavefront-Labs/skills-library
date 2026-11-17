---
id: computing-software.software-engineering.pnpm.task-concurrency-groups
name: task-concurrency-groups
category: computing-software
field: software-engineering
product: pnpm
tags: [concurrency-groups, task-priority, tasks-status, state-dir, machine-wide-limit, resume-from, dry-run-json]
level: advanced
status: docs-checked
description: "Cap task parallelism across processes with concurrencyGroups (v12.5.0), order waiting tasks by priority (v12.6.0), inspect with pnpm tasks status, use --resume-from."
sources:
  - https://pnpm.io/workspace-task-orchestration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
tasks:
  test:rust:
    concurrencyGroup: cargo
    dependsOn: []
concurrencyGroups:
  cargo: 2
```

At most 2 `cargo` tasks run at once across all pnpm processes sharing the same `stateDir` (including `pnpm pipeline`). Slots free when the process ends, even on a crash; a nested `pnpm run` in the group reuses its parent's slot. A different `stateDir` is a separate pool. A missing or zero limit restricts nothing. Use the same limit in workspaces sharing a group, since each process honours its own.

Priority (v12.6.0, default 0, integer): waiting tasks take free group slots in descending `priority`; negatives run last; ties go by arrival.

```yaml
tasks:
  build:critical: { concurrencyGroup: build, priority: 10 }
```

`pnpm tasks status` lists running and waiting tasks per group. A package script named `tasks` wins; use `pnpm pm tasks status`.

`--resume-from <pkg>` skips tasks the record of the same invocation says passed; without a usable record it omits that package's transitive dependencies (valid after a failed run, not a cancelled one). `pnpm -r run --dry-run --json test` prints `tasks[]` with `project`, `script`, `missingScript`, `dependsOn`.

## Checked

2026-11-04. Confirmed concurrencyGroups (v12.5.0), slot sharing rules, priority (v12.6.0), pnpm tasks status, --resume-from fallback and the --dry-run --json fields against pnpm.io/workspace-task-orchestration. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
