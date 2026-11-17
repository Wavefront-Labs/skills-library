---
id: computing-software.devops-ci-cd.nomad.affinity-block
name: affinity-block
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, affinity-block, affinity, anti-affinity, weight, node-scoring, placement, set-contains-all, regexp, version, hcl]
level: practitioner
status: docs-checked
description: "Express soft Nomad placement preferences with affinity blocks, weights from -100 to 100, operators, and read scoring in nomad alloc status -verbose."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/docs/job-specification/affinity.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nomad affinity block

`affinity` states a **preference** for nodes (unlike `constraint`, placement still succeeds if nothing matches). Valid at `job`, `group` and `task` level; task-level affinities apply to the whole task group. Nodes matching an affinity get a boosted score, combined with bin packing and other factors. Updating affinity is a non-destructive change.

```hcl
affinity {
  attribute = "${node.datacenter}"
  value     = "us-west1"
  weight    = 100
}
```

## Parameters
- `attribute` - interpolated node value (`${attr.*}`, `${meta.*}`, `${node.*}`).
- `operator` (default `"="`) - `=`, `!=`, `>`, `>=`, `<`, `<=`, `regexp`, `set_contains_all`, `set_contains_any`, `version`. Ordering is lexical. `set_contains` is the same as `set_contains_all`.
- `value` - required.
- `weight` (default `50`) - integer from -100 to 100. Negative weights are anti-affinities (matching nodes score lower). Use weights to rank several affinities.

## Examples
```hcl
affinity {
  attribute = "${attr.kernel.version}"
  operator  = "version"
  value     = "> 3.19"
  weight    = 50
}
affinity {
  attribute = "${meta.rack}"
  value     = "rack1"
  weight    = 50
}
```

## Seeing why a node was chosen
`nomad alloc status -verbose <alloc-id>` prints Placement Metrics with columns `binpack`, `job-anti-affinity`, `node-reschedule-penalty`, `node-affinity` and `final score`. `node-affinity` is non-zero only when the block matched. `job-anti-affinity` penalises extra instances of the same job on one node; `node-reschedule-penalty` steers away from nodes where the job already failed.

## Choosing
Use `constraint` (`computing-software.devops-ci-cd.nomad.constraint-block`) for hard requirements, `affinity` for ranking, and `spread` (`computing-software.devops-ci-cd.nomad.spread-block`) for distributing across values.

## Checked

2026-11-03. Confirmed against the affinity job-specification page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: nothing; no unsupported claim found.

Method: documentation only; no commands were run.
