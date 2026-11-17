---
id: computing-software.devops-ci-cd.nomad.migrate-block
name: migrate-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, migrate-block, migrate, drain, max-parallel, health-check, min-healthy-time, healthy-deadline, service-jobs, hcl]
level: practitioner
status: docs-checked
description: "Configure the Nomad migrate block that paces moving allocations off draining nodes with max_parallel, health_check, min_healthy_time, healthy_deadline and drain deadline override."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/migrate.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad migrate block

`migrate` sets how a group's allocations move off **draining** nodes (`nomad node drain`). Valid at `job` and `group` level; job-level applies to all groups. Only **service** jobs with `count` greater than 1 support it; if omitted a default strategy is used. Lost nodes (replace) and tasks failing beyond `restart` (reschedule) ignore it.

```hcl
migrate {
  max_parallel     = 1
  health_check     = "checks"
  min_healthy_time = "10s"
  healthy_deadline = "5m"
}
```

## Behaviour
While nodes drain, at most `max_parallel` allocations are stopped at once. The drain does not continue until each replacement has been healthy for `min_healthy_time`, or `healthy_deadline` is hit.

## Parameters (defaults)
- `max_parallel` (`1`) - must be less than the group `count`, since `count - max_parallel` allocations stay running.
- `health_check` (`"checks"`) - `"checks"` means all tasks running and their service checks healthy; `"task_states"` only requires tasks running (checks is a superset).
- `min_healthy_time` (`"10s"`) - time healthy before the allocation counts and unblocks the next migration.
- `healthy_deadline` (`"5m"`) - after this the allocation is marked unhealthy.

## Gotcha
A node drain's own deadline overrides the `migrate` block: the job author controls pacing, but the operator's deadline is the hard limit. See `computing-software.devops-ci-cd.nomad.node-drain`.

## Checked

2026-11-03. Confirmed against the migrate job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
