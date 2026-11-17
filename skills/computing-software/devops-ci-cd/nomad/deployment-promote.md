---
id: computing-software.devops-ci-cd.nomad.deployment-promote
name: deployment-promote
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, deployment-promote, promote, canary, deployment, group-flag, detach, manual-promotion, cli]
level: practitioner
status: docs-checked
description: "Promote healthy Nomad canaries with nomad deployment promote, select groups with -group, understand what it unblocks, and know the fail and revert alternatives."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/deployment/promote.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad deployment promote

Promotes the canaries of a deployment so the rolling upgrade of the remaining allocations is unblocked. Run it once canaries are healthy; with `update { canary = N }` and `auto_promote = false` the deployment otherwise waits (`Description = Deployment is running but requires manual promotion`).

```
nomad deployment promote 9fa81f27
nomad deployment promote -group web 9fa81f27
```
Takes a deployment ID or prefix. With no `-group`, all task groups are promoted; `-group` can be repeated to select some.

## Options
- `-group` - repeatable.
- `-detach` - return an evaluation ID (use `nomad eval status`).
- `-verbose`.

## ACLs
`submit-job` and `read-job` in the deployment's namespace.

## Workflow
1. `nomad status <job>` shows `Latest Deployment` and a table with `Promoted`, `Desired`, `Canaries`, `Placed`, `Healthy`, `Unhealthy` per group.
2. Verify canary health (service checks, logs).
3. Promote. Afterwards the old-version allocations are replaced in batches of `max_parallel`, and the deployment turns `successful`.

## If canaries are unhealthy
- `nomad deployment fail <id>` to fail the deployment.
- Fail forward by submitting a new job version.
- Fail backward with `nomad job revert` (`computing-software.devops-ci-cd.nomad.job-revert`).

`nomad job promote <job-id>` is the job-level shortcut used in the update block docs. See `computing-software.devops-ci-cd.nomad.update-block`.

## Checked

2026-11-03. Confirmed against the commands/deployment/promote page and the update job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
