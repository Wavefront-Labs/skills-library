---
id: computing-software.devops-ci-cd.nomad.numa-block
name: numa-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, numa-block, numa, cpu-cores, core-pinning, affinity, require, prefer, enterprise, device-colocation, hcl]
level: advanced
status: docs-checked
description: "Pin Nomad tasks to CPU cores on one NUMA node with the numa block affinity none, prefer or require and device colocation, plus the fragmentation trade-off."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/numa.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad numa block

`numa` (inside `resources`) makes core assignment aware of NUMA topology for memory-latency-sensitive workloads. NUMA-aware scheduling is limited to Linux, and it requires the task to request CPU with `cores` rather than `cpu`.

```hcl
resources {
  cores  = 4
  memory = 2048
  device "nvidia/gpu/1080ti" {
    count = 1
  }
  numa {
    affinity = "require"
    devices  = ["nvidia/gpu/1080ti"]
  }
}
```

## Parameters
- `affinity` (`"none"`):
  - `none`: any strategy; Nomad bin-packs cores onto NUMA nodes with the fewest available cores to limit fragmentation.
  - `prefer`: minimise total distance between cores, but they may span NUMA nodes.
  - `require`: cores strictly on one NUMA node. If no node has enough compatible cores, placement fails as resources exhausted.
- `devices` - devices that must sit on the same NUMA node as the cores. Must be a subset of devices in the `resources` block and works only with `affinity = "require"`.

## Trade-off
`require` fragments core availability per NUMA node; a cluster where every job uses it cannot pack efficiently. Reserve it for latency-sensitive jobs.

## Failure mode
The `numa` block requires the task to request CPU with `cores`; `cores` cannot be combined with `cpu` (`computing-software.devops-ci-cd.nomad.resources-block`).

## Checked

2026-11-03. Confirmed against the Nomad 1.10 numa job specification page: affinity values, devices subset rule, cores requirement, Linux limit, fragmentation warning, the GPU example. Removed: the Nomad Enterprise label and the cores plus cpu validation claim (that is on the resources page).

Method: documentation only; no commands were run.
