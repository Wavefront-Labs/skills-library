---
id: computing-software.cloud-infrastructure-engineering.google-cloud.sole-tenant-node-types-sizing-and-billing
name: sole-tenant-node-types-sizing-and-billing
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sole-tenant-nodes, sole-tenant-node-types, sole-tenant-billing, sole-tenancy-premium, capacity-planning, cud]
level: practitioner
status: docs-checked
description: "Pick sole-tenant node types and counts: node capacity vs VM packing, the sole-tenancy premium, CUD and sustained use effects, and headroom for host maintenance."
sources: ["https://docs.cloud.google.com/compute/docs/nodes/sole-tenant-nodes", "https://cloud.google.com/compute/sole-tenant-pricing", "https://docs.cloud.google.com/compute/docs/nodes/overcommitting-cpus-sole-tenant-vms", "https://docs.cloud.google.com/sdk/gcloud/reference/compute/sole-tenancy/node-types/list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sole-tenant node types, sizing and billing

## Node types
```bash
gcloud compute sole-tenancy node-types list --filter="zone:europe-west2-a" \
  --format="table(name,guestCpus,memoryMb,localSsdGb)"
# e.g. n2-node-80-640 (80 vCPU, 640 GB), c2-node-60-240, n2d-node-224-896, m1-node-96-1433
```
The name encodes series, vCPUs and memory in GB. The overview page lists every node type with processor, vCPU, memory and "Max VMs allowed"; `node-types list` shows what your project can use in a zone.

VMs on a node must use the same machine series as the node type (n2 nodes take n2 machine types), in predefined, custom or extended-memory shapes, until the node's vCPUs or memory are used up. C3 and C4 nodes also need the same vCPU-to-memory ratio as the node type. Nodes of C3, C3D, C4, C4A, C4D, G4, N4 and M4 are NUMA-aligned, so mixing full and sub-NUMA shapes can fragment capacity.

## Sizing
1. List target VMs with vCPU/RAM; pack per node by whichever dimension fills first.
2. Leave headroom for maintenance. The `migrate-within-node-group` policy reserves holdback nodes for live migration (1 for 2 to 20 nodes in the group, more for larger groups; a group needs at least 2 nodes) and you cannot delete the only empty node.
3. CPU overcommit (node template `--cpu-overcommit-type=enabled`, per-VM `--min-node-cpu`) lets the minimum guaranteed CPUs be as low as half the VM's CPUs (maximum node overcommit ratio 2.0). It needs an overcommit-enabled template from creation, only N1, N2, N2D and N4 nodes support it, and it suits bursty, uncorrelated workloads. Quota counts the node's vCPUs, not the overcommitted total.
4. Node group autoscaler: see the sole-tenant-node-group-autoscaling skill; check your licence terms before letting node counts change.

## Billing
- You pay for all vCPU and memory of the node plus a **sole-tenancy premium** computed on those resources, whether VMs fill the node or not. Read the rate on the pricing page; it is not repeated here.
- VMs placed on the node cost nothing extra. Disks and premium images are still billed.
- Sustained use discounts apply to the premium; flexible CUDs apply to the node and the premium; resource-based CUDs cover vCPU and memory but not the premium.
- Nodes with CPU overcommit enabled on the template carry an additional premium, fixed regardless of overcommit level.
- Nodes with GPUs or Local SSD bill for all of those devices, and the premium excludes them.
- Charges have a one-minute minimum, then per-second billing.

## Example
Twelve VMs of 16 vCPU / 64 GB need 192 vCPU / 768 GB. An `n2-node-80-640` holds 5 such VMs by vCPU (80/16) and 10 by memory (640/64), so it is CPU-bound: 3 nodes give 15 slots and 3 spare slots.

## Gotchas
- Node types are available in select zones; list them per zone before committing.
- Sole-tenant VMs cannot use T2D, T2A, E2, C2D, A3 Ultra, A3 Edge, A4, A4X or bare metal, cannot specify a minimum CPU platform, and are not preemptible.
- You cannot change the maintenance policy of a live node group.

## Verify
- [ ] Billing export shows node SKUs and the premium SKU matching the plan.

## Checked
2026-10-28. Confirmed against the Sole-tenancy overview (node type naming and table, same-series rule, C3/C4 ratio and NUMA notes, holdback table, restrictions, pricing structure), the sole-tenant pricing page (premium basis, discount interaction, one-minute minimum then per-second), the CPU overcommit page (2.0 ratio, supported series, extra premium, flag names) and the Compute API NodeType schema (`guestCpus`, `memoryMb`, `localSsdGb`). Removed: premium percentages, the 70% utilisation target, the unsourced "system reserve" and reservation claims. The pricing page itself was not relied on for any rate.
Method: documentation only; no commands were run.
