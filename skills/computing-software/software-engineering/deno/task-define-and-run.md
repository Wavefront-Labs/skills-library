---
id: computing-software.software-engineering.deno.task-define-and-run
name: task-define-and-run
category: computing-software
field: software-engineering
product: deno
tags: [task, tasks-field, if-present, init-cwd, env-file, task-runner]
level: intro
status: docs-checked
description: "Define deno.json tasks, run them with deno task, skip missing tasks with --if-present, use INIT_CWD for the caller's directory, and load dotenv files."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/cli/task.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`deno task` is a cross-platform task runner. Define commands under `"tasks"` in the config file; a task is a string or an object with `command` and `description`:

```jsonc title="deno.json"
{
  "tasks": {
    "data": "deno task collect && deno task analyze",
    "collect": "deno run --allow-read=. --allow-write=. scripts/collect.js",
    "analyze": {
      "description": "Run analysis script",
      "command": "deno run --allow-read=. scripts/analyze.js"
    }
  }
}
```

A bare `deno task` lists tasks. A missing named task exits non-zero; `--if-present` makes it exit 0 silently (handy in shared CI scripts):

```sh
deno task --if-present build
```

The working directory is the directory of the config file. `INIT_CWD` holds the directory the task was run from (like `npm run`):

```json title="deno.json"
{
  "tasks": {
    "start": "deno run main.ts \"$INIT_CWD\""
  }
}
```

Load dotenv files into the task shell with `--env-file` (defaults to `.env`; repeatable, later files win):

```sh
deno task --env-file=.env.production start
```

To force npm, call it in the task: `"test:node": "npm run test"`.

## Checked

2026-11-04. Confirmed against docs runtime/reference/cli/task.md (deno task): tasks key with string or command/description object, --if-present, INIT_CWD and config-directory cwd, --env-file defaults and precedence, npm run in a task.

Method: documentation only; no commands were run.
