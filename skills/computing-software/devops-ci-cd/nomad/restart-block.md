---
id: computing-software.devops-ci-cd.nomad.restart-block
name: restart-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, restart-policy, restart, attempts, interval, delay, mode, render-templates, task-failure, hcl, job-spec]
level: practitioner
status: docs-checked
description: "Configure the Nomad restart block with attempts, interval, delay, mode fail or delay, render_templates, job-type defaults, group-versus-task merging and disabling restarts."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/restart.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad restart block (restart-policy)

The `restart` block controls what the **client** does when a task fails, on the same node. It is distinct from `reschedule`, which moves the allocation to another node once restarts are exhausted (see `computing-software.devops-ci-cd.nomad.reschedule-block`). It may appear in `group` or `task`.

```hcl
group "example" {
  restart {
    attempts = 3
    delay    = "30s"
  }
}
```

## Parameters and defaults
- `attempts` - restarts allowed within `interval`. Default varies by job type.
- `interval` - window that opens when the first task starts; more than `attempts` failures inside it triggers `mode`.
- `delay` - default `"15s"`; up to 25% random jitter is added.
- `mode` - default `"fail"`. `"fail"` stops restarting, marks the allocation failed, and hands it to the `reschedule` block (right for non-idempotent work). `"delay"` waits until another `interval` and tries again, so the allocation never fails because of restarts.
- `render_templates` - default `false`; `true` re-renders all `template` blocks on each restart, useful to re-fetch Vault secrets even if their lease has not expired.

Per-type defaults: batch is `attempts = 3`, `interval = "24h"`, `delay = "15s"`, `mode = "fail"`. Service and system are `attempts = 2`, `interval = "30m"`, `delay = "15s"`, `mode = "fail"`.

## Group versus task
A group-level policy is inherited by every task (including sidecars). A task-level block is merged field by field over the group one: group `interval = "30m"`, `attempts = 2` plus a task `attempts = 5` yields attempts 5 with the group's interval. Sidecar tasks do not accept a `restart` block, so for jobs with Connect sidecars set `restart` at the task level so the sidecar inherits the default.

## Disable restarts
```hcl
restart {
  attempts = 0
  mode     = "fail"
}
```

## Example of delay mode
`attempts = 3`, `delay = "15s"`, `interval = "10m"`, `mode = "delay"`: three quick restarts, then a wait until the 10-minute interval passes, then three more. The allocation is never failed by the restart policy.

## Gotchas
- With `mode = "fail"` a task that fails again inside the interval fails the whole allocation; what happens next depends on `reschedule`, not `restart`.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 restart job specification page: attempts, delay (15s, 25% jitter), interval, mode, render_templates, batch and service defaults, group and task merge, sidecar advice, disabling, both mode examples. Removed: the claim that restarted tasks keep old template output by default.

Method: documentation only; no commands were run.
