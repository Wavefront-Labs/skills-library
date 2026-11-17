---
id: computing-software.devops-ci-cd.nomad.resources-block
name: resources-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, resources-block, resources, cpu, cores, memory, memory-max, memory-oversubscription, secrets, cgroup, hcl]
level: practitioner
status: docs-checked
description: "Size Nomad tasks with the resources block covering cpu MHz, reserved cores, memory, memory_max oversubscription, secrets tmpfs size and devices."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/resources.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad resources block

`resources` (task level) states what a task needs; the scheduler places on `cpu`/`memory`.

```hcl
resources {
  cpu    = 100
  memory = 256
  device "nvidia/gpu" {
    count = 2
  }
}
```

## Parameters (defaults)
- `cpu` (`100`) - MHz.
- `cores` - reserve whole cores exclusively; shares no CPU time with other Nomad tasks. Behaviour is per driver (docker, exec). Setting `cores` together with `cpu` fails job validation.
- `memory` (`300`) - MB.
- `memory_max` - optional hard cap in MB for oversubscription.
- `numa` - NUMA preference, requires `cores` (`computing-software.devops-ci-cd.nomad.numa-block`).
- `device` - repeatable device request (`computing-software.devops-ci-cd.nomad.device-block`).
- `secrets` - size in MB of the `secrets/` tmpfs directory. When set it is added to `memory` for scheduling and shown in `nomad alloc status` and `nomad node status`. If unset, 1 MB of tmpfs is used and not counted. Do not set it where tmpfs is unsupported, because it is still counted.

## Memory oversubscription
Drivers apply a hard **limit** (Linux `memory.max` cgroup) and a soft **reservation** (`memory.low`). With `memory_max` set, `memory` becomes the reservation and `memory_max` the hard limit; without it `memory` is the hard limit. Supported by the `raw_exec`, `exec2`, `exec`, `docker`, `podman` and `java` drivers. It is opt-in: operators enable it in the scheduler configuration (`MemoryOversubscriptionEnabled`); Enterprise can restrict it with quotas and per node pool.

Under contention the OS pressures tasks and Nomad may kill oversubscribed tasks and reschedule them. Mitigate by setting `oom_score_adj` for non-Nomad host services, alerting on OOM, and making the client `reserved` memory cover host services plus the expected excess (with 1 GB reserved, allocations may collectively exceed their soft limits by almost 1 GB before contention). Scheduling uses `memory` only.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 resources job specification page: cpu, cores, memory, memory_max, numa, device and secrets semantics, memory oversubscription limits, supported drivers, the mitigation advice. Nothing removed.

Method: documentation only; no commands were run.
