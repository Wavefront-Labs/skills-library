---
id: computing-software.devops-ci-cd.nomad.update-block
name: update-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, update-strategy, update, rolling-update, canary, blue-green, auto-revert, auto-promote, progress-deadline, max-parallel, stagger, hcl]
level: practitioner
status: docs-checked
description: "Configure the Nomad update block for rolling, canary and blue/green deployments with max_parallel, health_check, deadlines, auto_revert, auto_promote and stagger."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/update.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad update block (update-strategy)

`update` sets the rolling-upgrade and canary strategy for a group. Valid at `job` and `group` level; blocks merge with group beating job, so put shared values at job level and only differences in groups.

```hcl
update {
  max_parallel      = 3
  health_check      = "checks"
  min_healthy_time  = "10s"
  healthy_deadline  = "5m"
  progress_deadline = "10m"
  auto_revert       = true
  auto_promote      = true
  canary            = 1
  stagger           = "30s"
}
```

## Parameters (defaults)
- `max_parallel` (`1`) - allocations updated at once per group. `0` means forced updates instead of deployments.
- `health_check` (`"checks"`) - `checks`, `task_states`, or `manual` (you set health through the deployments HTTP API).
- `min_healthy_time` (`"10s"`) - healthy time before the next batch is unblocked.
- `healthy_deadline` (`"5m"`) - then the allocation turns unhealthy. If `progress_deadline` is non-zero it must be greater than this, otherwise the deployment can fail before an allocation reaches its deadline.
- `progress_deadline` (`"10m"`) - starts at the first allocation, resets on each allocation turning healthy or on promotion; if nothing turns healthy the deployment fails. `0` fails on the first unhealthy allocation.
- `auto_revert` (`false`) - roll back to the last stable job on failure (stable = every allocation of its deployment was healthy).
- `auto_promote` (`false`) - promote canaries once all are healthy; with several groups, all must set it.
- `canary` (`0`) - number of new allocations to start without stopping old ones. Cannot be used with volumes that have `per_alloc = true`.
- `stagger` (`"30s"`) - delay between batches for **system** jobs only; for system jobs only `max_parallel` and `stagger` are enforced.

## Patterns
- Canary: `canary = 1`, `max_parallel = 3`, then promote with `nomad job promote <job-id>` (see `computing-software.devops-ci-cd.nomad.deployment-promote`); the rolling update of the rest then proceeds at `max_parallel`.
- Blue/green: set `canary` equal to the group `count` (for example both 3). The full new set runs beside the old one, doubling resources until promoted; promotion shuts the old allocations down.
- Serial: `max_parallel = 1`.

## Inheritance example
Job-level `max_parallel = 2`, `health_check = "task_states"`, `healthy_deadline = "10m"` plus a group-level `canary = 1` gives that group all four values.

## Checked

2026-11-03. Confirmed against the update job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
