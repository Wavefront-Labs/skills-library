---
id: computing-software.devops-ci-cd.nomad.group-block
name: group-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, group-block, group, count, shutdown-delay, co-location, task-group, job-spec, hcl]
level: practitioner
status: docs-checked
description: "Structure a Nomad group block that co-locates tasks on one client, with count, shutdown_delay, per-group constraint, network, service and the sub-blocks a group accepts."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/group.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad group block

`group "<name>"` is the unit of scheduling: **every task in a group is placed on the same client**. Placing conflicting per-task constraints in one group therefore makes it unplaceable (see `computing-software.devops-ci-cd.nomad.constraint-block`).

```hcl
group "example" {
  count = 5
  constraint {
    attribute = "${attr.cpu.arch}"
    value     = "amd64"
  }
  network {
    mode = "bridge"
    port "http" {}
    port "lb" { static = "8889" }
  }
  task "cache" { # ... }
}
```

## Parameters
- `count` - non-negative; defaults to the `scaling` block's `min` if present, otherwise `1`.
- `shutdown_delay` (`"0s"`) - wait between Consul/Nomad service deregistration and sending the shutdown signal, so in-flight requests finish or health checks fail first. At group level it runs regardless of whether services are defined and applies to group services; tasks have their own `shutdown_delay` that waits between deregistering task services and stopping the task.
- `task` (required, repeatable).
- Sub-blocks accepted: `constraint`, `affinity`, `spread`, `consul`, `ephemeral_disk`, `disconnect`, `meta`, `migrate`, `network`, `reschedule`, `restart`, `service`, `update`, `vault`, `volume`.

## Notes on specific blocks
- `consul` applies to all tasks and services unless a task has its own.
- `restart` omitted means the job-type default (`computing-software.devops-ci-cd.nomad.restart-block`).
- `vault` here overrides a job-level one for all tasks.
- `migrate` applies only to service jobs with `count > 1`.
- `service` registers when the allocation starts and deregisters when it is destroyed:

```hcl
service {
  name = "example"
  port = "api"
  tags = ["default"]
  check {
    type     = "tcp"
    interval = "10s"
    timeout  = "2s"
  }
}
```

## Checked

2026-11-03. Confirmed against the group job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
