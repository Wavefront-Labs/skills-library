---
id: computing-software.devops-ci-cd.nomad.node-eligibility
name: node-eligibility
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, node-eligibility, eligibility, ineligible, scheduling-eligibility, cordon, drain, maintenance, cli]
level: intro
status: docs-checked
description: "Toggle whether a Nomad client accepts new allocations with nomad node eligibility -enable or -disable, and why to disable eligibility on all nodes before a multi-node drain."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/node/eligibility.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad node eligibility

Toggles scheduling eligibility for a node. Nodes are eligible by default; an ineligible node cannot receive new placements.

```
nomad node eligibility -disable <node-id-prefix>
nomad node eligibility -enable <node-id-prefix>
nomad node eligibility -disable -self
```
Pass `-enable` or `-disable`, plus a node ID or prefix, or `-self`. An ambiguous prefix lists the matching nodes. `-yes` auto-confirms. ACL: `node:write`. Output looks like `Node "..." scheduling eligibility set: ineligible for scheduling`.

## Interaction with drain
- `nomad node drain -enable` disables eligibility automatically; disabling a drain restores it (unless `-keep-ineligible`).
- Before draining a set of nodes, mark every one ineligible first. Otherwise allocations drained from the first node may be placed on a node that is about to be drained, and get rescheduled several times.

## Other use
Mark a misbehaving node ineligible to inspect it without risk of new work arriving.

See `computing-software.devops-ci-cd.nomad.node-drain`.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 node eligibility command page: -enable, -disable, -self, -yes, node:write, output text, drain interaction and the multi-node drain advice; node drain page for -keep-ineligible. Removed: the cordon comparison and the running-allocations claim.

Method: documentation only; no commands were run.
