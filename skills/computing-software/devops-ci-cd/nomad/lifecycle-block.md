---
id: computing-software.devops-ci-cd.nomad.lifecycle-block
name: lifecycle-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, task-lifecycle, lifecycle, prestart, poststart, poststop, sidecar, init-task, task-dependencies, shutdown-order, hcl]
level: practitioner
status: docs-checked
description: "Order Nomad tasks inside a group with the lifecycle block using hook prestart, poststart or poststop and sidecar true or false, including init, companion and cleanup patterns."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/lifecycle.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad lifecycle block (task-lifecycle)

`lifecycle` (inside a `task`) controls when a task runs relative to the group's **main tasks** (tasks without a `lifecycle` block).

## Parameters
- `hook` (required) - `prestart`: starts immediately, and main tasks wait until every prestart task with `sidecar = false` has completed successfully. `poststart`: starts once all main tasks are running. `poststop`: starts after main tasks have stopped successfully or exhausted their `restart` retries.
- `sidecar` (default `false`) - `false` means ephemeral: not restarted after it exits successfully. `true` means long-lived: restarted for as long as the allocation runs.

## Stop order
Nomad waits for the group's `shutdown_delay`, stops the `leader` task if one exists, then stops non-sidecar, non-poststop tasks, and finally the sidecar tasks.

## Patterns
Init task (blocks the main task until a dependency is reachable):
```hcl
task "wait-for-db" {
  lifecycle {
    hook    = "prestart"
    sidecar = false
  }
  driver = "exec"
  config {
    command = "sh"
    args    = ["-c", "while ! nc -z db.service.local.consul 8080; do sleep 1; done"]
  }
}
```
Companion sidecar (log shipper or proxy sharing the allocation's filesystem and network):
```hcl
task "fluentd" {
  lifecycle {
    hook    = "poststart"
    sidecar = true
  }
  driver = "docker"
  config { image = "fluentd/fluentd" }
}
```
Cleanup: `hook = "poststop"` for a task that posts a notification or post-processes after the main tasks end.

Use init tasks only when `template` or `artifact` cannot do the job.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 lifecycle job specification page: hooks, sidecar semantics, stop order, the init, companion and cleanup patterns. Removed: the never-exiting prestart failure-mode advice.

Method: documentation only; no commands were run.
