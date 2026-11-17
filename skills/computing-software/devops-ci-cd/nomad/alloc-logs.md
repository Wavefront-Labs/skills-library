---
id: computing-software.devops-ci-cd.nomad.alloc-logs
name: alloc-logs
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, alloc-logs, logs, stdout, stderr, follow, tail, job-flag, read-logs, cli]
level: intro
status: docs-checked
description: "Read Nomad task logs with nomad alloc logs using -stderr, -f follow, -tail with -n or -c, -job random allocation selection, and the read-logs ACL capability."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/alloc/logs.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad alloc logs

Alias: `nomad logs`. Streams a task's stdout or stderr.

```
nomad alloc logs [options] <allocation> [<task>]
nomad alloc logs -stderr eb17e557 redis
nomad alloc logs -tail -n 2 eb17e557 redis
nomad alloc logs -f -job example
```
The task can be omitted for single-task allocations. `-task` takes precedence if you give both the option and the argument (the argument is ignored).

## Options
- `-stdout` (default, except with `-f`) and `-stderr`.
- `-f` - follow. With only `-job` and/or `-task` it follows **both** stdout and stderr.
- `-tail` - read relative to the end; `-n <lines>` (default 10 with `-tail`) or `-c <bytes>` set the offset.
- `-job=<name|id prefix>` - pick a random allocation of the job, preferring a running one but falling back to a dead allocation. `-group` narrows which group's task.
- `-verbose`.

## ACLs
`read-logs`, `read-job` and `list-jobs` in the allocation's namespace.

## Gotchas
- `-no-color` only affects Nomad's own output; escape sequences in the task output are passed through.
- If the task's `logs` block has `disabled = true`, the command returns 404 (`computing-software.devops-ci-cd.nomad.logs-block`).
- With `-job`, you may be reading a different instance each time; pass an allocation ID when comparing runs.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 alloc logs command page: options and defaults, -f behaviour, -tail with -n default 10, -job selection, ACL capabilities, -no-color note. Nothing removed.

Method: documentation only; no commands were run.
