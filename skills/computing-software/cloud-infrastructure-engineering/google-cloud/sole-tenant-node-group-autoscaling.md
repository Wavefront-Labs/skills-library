---
id: computing-software.cloud-infrastructure-engineering.google-cloud.sole-tenant-node-group-autoscaling
name: sole-tenant-node-group-autoscaling
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sole-tenant-nodes, node-group-autoscaling, node-groups, byol, capacity-planning]
level: advanced
status: docs-checked
description: "Configure the sole-tenant node group autoscaler: on vs only-scale-out modes, min/max nodes, interaction with BYOL licence counts, maintenance policies and placement."
sources: ["https://docs.cloud.google.com/compute/docs/nodes/autoscaling-node-groups", "https://docs.cloud.google.com/compute/docs/nodes/provisioning-sole-tenant-vms", "https://docs.cloud.google.com/sdk/gcloud/reference/compute/sole-tenancy/node-groups/update"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sole-tenant node group autoscaling

## 1. Modes
| `--autoscaler-mode` | Behaviour | Use |
|---|---|---|
| `on` | scales out when a VM cannot be scheduled; scales in when a node stays empty | general sole tenancy |
| `only-scale-out` | adds nodes, never removes empty ones | monotonically growing or physical-server-affinity workloads such as BYOL; required with the `migrate-within-node-group` maintenance policy |
| `off` | autoscaler disabled; you size the group | strict licence/host audits |

The autoscaler is not enabled by default. `--min-nodes` defaults to 0; `--max-nodes` must be at least `--min-nodes` and at most 100 (the maximum node group size).

```bash
gcloud compute sole-tenancy node-groups create byol-ng --zone=<Z> \
  --node-template=n2-byol-tmpl --target-size=2 \
  --autoscaler-mode=only-scale-out --min-nodes=2 --max-nodes=6 \
  --maintenance-policy=restart-in-place
gcloud compute sole-tenancy node-groups update byol-ng --zone=<Z> --autoscaler-mode=on --max-nodes=8
gcloud compute sole-tenancy node-groups describe byol-ng --zone=<Z> --format='yaml(autoscalingPolicy,size)'
```

## 2. How scale-out is triggered
Scale-out happens when scheduling a VM fails for lack of capacity: a node is added and the operation is retried. The decision uses the VM's size, the free capacity on the target nodes (node size, VMs already placed, and the optional CPU overcommit ratio) and the group's autoscaling policy; it does not use CPU utilisation inside nodes.

## 3. Licensing interaction
- Per-core or per-host BYOL: every added node adds hardware to license, so `max-nodes` is your licence ceiling. Google recommends `only-scale-out` for workloads that need licences tied to the same physical server.
- Scale-in (`on`) is triggered when a node stays empty for a period; an empty node is scheduled for removal after a stabilisation period. A node empties when its VMs are deleted or migrated out, so delete or move VMs yourself if you want to shrink.
- With `only-scale-out`, manual increases of group size are disabled; you can shrink by emptying a node and then removing it.
- To list the current nodes for licence reporting: `gcloud compute sole-tenancy node-groups list-nodes <GROUP> --zone=<Z>`. It shows the present state, so record counts yourself if you need history.

## Gotchas
- `migrate-within-node-group` requires `only-scale-out` on autoscaled groups.
- To force growth manually on an autoscaled group, raise `--min-nodes` above the current size.
- To exceed 100 nodes, create several node groups with a matching affinity label and enable the autoscaler on each.
- The autoscaler works only in regions that support sole-tenant nodes.
- CPU overcommit changes how many VMs fit; re-test autoscaler assumptions when enabling it.

## Verify
- [ ] Creating one more VM than fits triggers a new node and the VM lands on it.
- [ ] Node count never exceeds the licensed maximum.

## Checked
2026-10-28. Confirmed against the "Autoscale node groups" page: modes and their wording, min default 0, max at most 100, scale-out and scale-in triggers, the `migrate-within-node-group` requirement for `only-scale-out`, manual resize rules, the multi-group affinity workaround, the region note, and the gcloud commands and flags (checked against the gcloud reference). Removed: scale-out timing, named licence products, a headroom rule, a capacity-error claim and packing advice, none of which the page states.
Method: documentation only; no commands were run.
