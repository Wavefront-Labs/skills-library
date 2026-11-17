---
id: computing-software.software-engineering.deno.task-dependencies-and-wildcards
name: task-dependencies-and-wildcards
category: computing-software
field: software-engineering
product: deno
tags: [task, dependencies, wildcard, parallel, jobs, cycle-detection]
level: practitioner
status: docs-checked
description: "Task dependencies that run in parallel, deduplication and cycle errors, grouping tasks without a command, wildcard patterns with exclusions, and --jobs."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/cli/task.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List `dependencies` on a task; they run in parallel first, then the task runs:

```json title="deno.json"
{
  "tasks": {
    "build": "deno run -RW build.ts",
    "generate": "deno run -RW generate.ts",
    "serve": {
      "command": "deno run -RN server.ts",
      "dependencies": ["build", "generate"]
    }
  }
}
```

A shared dependency runs once (diamond a->b,c->d runs d once). A cycle errors: `Task cycle detected: a -> b -> a`.

A task with `dependencies` but no `command` groups tasks, e.g. `"dev": { "dependencies": ["dev:client", "dev:server"] }`.

The parallel limit defaults to the number of cores. Override with `--jobs`/`-j` (alias `--concurrency`) or `DENO_JOBS`; the flag wins:

```sh
deno task --recursive --jobs 1 build
```

In Deno 2.8, parallel output lines are prefixed with the task name.

Wildcards run several tasks in parallel. Quote the pattern so the shell does not expand it:

```sh
deno task "build:*"
```

Use `:` as the multi-word separator (`build:client`, `test:unit`). Exclude with a group at the end:

```sh
deno task "test:*(!e2e|interactive)"
```

A pattern with an exclusion group but no `*` is rejected.

## Checked

2026-11-04. Confirmed against docs runtime/reference/cli/task.md (deno task): dependencies, parallel run, deduplication, cycle error text, command-less grouping tasks, --jobs/-j/--concurrency/DENO_JOBS, 2.8 output prefixes, wildcard and exclusion syntax.

Method: documentation only; no commands were run.
