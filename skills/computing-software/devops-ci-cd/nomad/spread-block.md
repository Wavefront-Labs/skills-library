---
id: computing-software.devops-ci-cd.nomad.spread-block
name: spread-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, spread-block, spread, failure-domains, target-percent, datacenter, rack, scheduling-performance, weight, hcl]
level: practitioner
status: docs-checked
description: "Spread Nomad allocations across datacenters or racks with spread blocks, target percentages and weights, and understand the scheduling-performance cost."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/spread.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad spread block

`spread` asks the scheduler to distribute a job's allocations across values of a node attribute (datacenter, availability zone, rack) for failure tolerance. It is a **soft** preference: placement still succeeds when criteria cannot be met, and distribution may be imperfect because not every node is scored. Valid at `job` and `group` level (job-level is inherited). Editing it is a non-destructive update.

Without `spread`, the scheduler already tries to put allocations of one job on different nodes and bin-packs across jobs.

```hcl
spread {
  attribute = "${node.datacenter}"
  weight    = 100
  target "us-east1" {
    percent = 60
  }
  target "us-west1" {
    percent = 40
  }
}
```

## Parameters
- `attribute` - interpolated node value.
- `target "<value>"` - with `percent` (integer); omit targets for an even spread. A single target (for example 50% to `us-east1`) leaves the rest spread over the other values.
- `weight` (integer 0 to 100, default 0) - ranks multiple spread or affinity blocks.

With `count = 10` over two datacenters, an even spread aims at 5 and 5; targets 60/40 aim at 6 and 4. Two spreads (datacenter and `${meta.rack}`, weight 50 each) with `count = 12` aim at 6 per datacenter, then 3 per rack.

## Not the same as the spread algorithm
The cluster/node-pool scheduler algorithm setting `"spread"` versus `"binpack"` affects how different jobs share nodes; the `spread` block only shapes one job.

## Performance cost
Normally the scheduler stops after a few feasible nodes (2 for batch; log2 of the node count in datacenter and pool, minimum 2, for service). With `spread` it scores a number of nodes equal to the group `count` (max 100) per allocation, which can multiply scheduling time by an order of magnitude. Watch `nomad.nomad.worker.invoke_scheduler.*` metrics; mitigate by dropping `spread` or shrinking the node pool/datacenter.

Works best on attributes with similar node counts (identical racks or similar datacenters).

## Checked

2026-11-03. Confirmed against the spread job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
