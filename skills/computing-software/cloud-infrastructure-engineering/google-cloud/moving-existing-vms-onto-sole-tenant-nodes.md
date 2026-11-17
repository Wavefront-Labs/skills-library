---
id: computing-software.cloud-infrastructure-engineering.google-cloud.moving-existing-vms-onto-sole-tenant-nodes
name: moving-existing-vms-onto-sole-tenant-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sole-tenant-nodes, sole-tenant-migration, move-vm-to-sole-tenant, node-affinity, set-scheduling]
level: practitioner
status: docs-checked
description: "Move existing Compute Engine VMs onto (or off) sole-tenant nodes by setting node affinity with set-scheduling, including constraints on machine series, CPU platform and GPUs."
sources: ["https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/set-scheduling", "https://docs.cloud.google.com/compute/docs/nodes/sole-tenant-nodes", "https://docs.cloud.google.com/compute/docs/nodes/provisioning-sole-tenant-vms", "https://docs.cloud.google.com/compute/docs/nodes/overcommitting-cpus-sole-tenant-vms"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Moving existing VMs onto sole-tenant nodes

## Steps
```bash
Z=europe-west2-a
# 1. node group must exist in the same zone with a node type whose series matches the VM (n2 VMs -> n2-node-80-640)
gcloud compute sole-tenancy node-groups describe licensed-ng --zone=$Z
# 2. stop the VM (set-scheduling works only on a stopped, TERMINATED instance)
gcloud compute instances stop sql-01 --zone=$Z
# 3. set affinity: node group, a specific node, or a labels file (one of these per call)
gcloud compute instances set-scheduling sql-01 --zone=$Z --node-group=licensed-ng
#   or: --node=<NODE>   or: --node-affinity-file=affinity.json
# 4. start
gcloud compute instances start sql-01 --zone=$Z
gcloud compute instances describe sql-01 --zone=$Z --format="value(scheduling.nodeAffinities)"
```
Affinity file: a JSON/YAML list of objects with `key`, `operator` (`IN` or `NOT_IN`) and `values`; rules filter nodes by the affinity labels their node template defines.

Off sole-tenancy: stop, `set-scheduling --clear-node-affinities`, start.

## Constraints
- The VM's machine series must match the node type (an N2 VM on an n2 node); predefined, custom and extended-memory shapes fit until node vCPUs or memory run out.
- A VM that specifies a minimum CPU platform cannot move onto a sole-tenant node: set the platform to automatic first.
- Sole-tenant VMs cannot be preemptible, and cannot use T2D, T2A, E2, C2D, A3 Ultra, A3 Edge, A4, A4X or bare metal machine types.
- A node with GPUs does not accept VMs without GPUs.
- The VM's on-host-maintenance setting must suit the node group's policy: `restart-in-place` needs `TERMINATE`; `migrate-within-node-group` needs the VM to target one node group by group name (not a single node), and `MIGRATE` is recommended.
- Capacity is not oversubscribed unless CPU overcommit is configured on the node template; per-VM `--min-node-cpu` (and `--clear-min-node-cpu`) set the guaranteed CPUs.

## Bulk approach
Script the loop above per VM. Instance templates can carry `--node-group`, or `--node-affinity-file` for regional MIGs spanning several node groups.

## Gotchas
- If the node group is full the start will fail; add capacity first (resize the group or enable the autoscaler).
- Moving changes the physical host. For licence reporting, record the new node.

## Verify
- [ ] `gcloud compute sole-tenancy node-groups list-nodes licensed-ng --zone=$Z` lists the VM on a node.

## Checked
2026-10-28. Confirmed against the gcloud `instances set-scheduling` reference (stopped-instance requirement, `--node`, `--node-group`, `--node-affinity-file` with `key`/`operator`/`values`, `--clear-node-affinities`, `--min-node-cpu`), the Sole-tenancy overview (restrictions, series match, GPU rule, maintenance policy notes), the BYOL page (restart-in-place needs TERMINATE; migrate-within-node-group needs node-group-name) and the provisioning page (MIG instance templates and `--node-affinity-file`). Removed: `--discard-local-ssd`, a named error string, Migrate to Virtual Machines and BYOL host-count claims, which no fetched page supports.
Method: documentation only; no commands were run.
