---
id: computing-software.software-engineering.deno.task-caching-and-workspaces
name: task-caching-and-workspaces
category: computing-software
field: software-engineering
product: deno
tags: [task, caching, files-output-env, workspace, recursive, filter]
level: advanced
status: docs-checked
description: "Skip unchanged tasks with files/output/env cache fields, and run tasks across workspace members with --recursive and --filter."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/cli/task.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Task result caching is opt-in: add `files` and Deno fingerprints the command, appended arguments, matching file contents and listed env vars, then skips the task when nothing changed. A task with no `files` always runs.

```jsonc title="deno.json"
{
  "tasks": {
    "build": {
      "command": "deno run -RW build.ts",
      "files": ["src/**/*.ts", "deno.json"],
      "output": ["dist/"],
      "env": ["NODE_ENV"]
    }
  }
}
```

- `files`: input globs forming the cache key.
- `output`: globs the task produces; restored from cache on a hit.
- `env`: variable names whose values are part of the key.

Dependency fingerprints are folded into the task's own key, so a task re-runs whenever an upstream one did.

Workspaces: `--recursive` runs the named task from all members in parallel.

```sh
deno task --recursive dev
```

Filter by member name (the `name` in each member's deno.json):

```sh
deno task --filter "client" dev
```

## Checked

2026-11-04. Confirmed against docs runtime/reference/cli/task.md (deno task): files/output/env cache fields, opt-in caching, dependency fingerprints, --recursive and --filter.

Method: documentation only; no commands were run.
