---
id: computing-software.devops-ci-cd.turborepo.turbo-json-persistent-interactive-interruptible-tasks
name: turbo-json-persistent-interactive-interruptible-tasks
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, persistent, interactive, interruptible, turbo-watch, long-running-tasks, stdin, outputlogs-values, cache-option]
level: practitioner
status: docs-checked
description: "Task options for long-running work: persistent blocks dependents, interactive accepts stdin, interruptible lets turbo watch restart, plus the outputLogs values."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`persistent`** (default `false`): labels a task as long-running so other tasks cannot depend on it. A process that never exits would make dependents never run, so `turbo` throws an error if another task depends on a persistent one. Most useful for dev servers and watchers. Persistent tasks are `interactive` by default.

**`interactive`** (default `false`, `true` for persistent tasks): accept `stdin` input in the terminal UI. Must be used with `persistent`. Useful for scripts you manipulate while running, such as Jest or Vitest.

```json
{ "tasks": { "test:watch": { "interactive": true, "persistent": true } } }
```

**`interruptible`** (default `false`): lets `turbo watch` restart a `persistent` task. `turbo watch` restarts affected tasks on changes, but persistent tasks are not restarted unless `interruptible` is `true`.

**`cache`** (default `true`): whether outputs are cached. `false` suits dev tasks and ensures a task always runs when it is in the execution graph.

**`outputLogs`** (default `full`; overridden by `--output-logs`):
- `full` displays all logs
- `hash-only` shows only task hashes
- `new-only` shows logs only from cache misses
- `errors-only` shows logs only from failures
- `none` hides all task logs

With `errors-only`, the `errorsOnlyShowHash` future flag shows hashes for successful tasks.

**`with`**: tasks run alongside this one, ideal for long-running tasks that must run together.

## Checked

2026-11-04. Read the `cache`, `outputLogs`, `persistent`, `interactive`, `interruptible` and `with` entries of the configuration reference in full; defaults, values and wording match. Removed the invented Verify step.

Method: documentation only; no commands were run.
