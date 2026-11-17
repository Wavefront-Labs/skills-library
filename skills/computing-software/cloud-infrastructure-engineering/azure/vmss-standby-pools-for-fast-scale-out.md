---
id: computing-software.cloud-infrastructure-engineering.azure.vmss-standby-pools-for-fast-scale-out
name: vmss-standby-pools-for-fast-scale-out
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vmss, standby-pool, flexible-orchestration, autoscale, scale-out]
level: practitioner
status: docs-checked
description: "Cut VMSS scale-out latency with standby pools: pre-provisioned running or deallocated VMs, ready capacity semantics, limitations and cost trade-offs."
sources: ["https://learn.microsoft.com/azure/virtual-machine-scale-sets/standby-pools-overview", "https://learn.microsoft.com/azure/virtual-machine-scale-sets/standby-pools-create", "https://learn.microsoft.com/cli/azure/standby-vm-pool"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VMSS standby pools

**Goal:** scale out faster when VMs need long boot/config times (large images, app warm-up).

## How it works
A standby pool attached to a scale set with **Flexible orchestration** keeps pre-provisioned VMs in a **running**,
**deallocated** (stopped) or hibernated (preview) state. On scale-out the scale set takes VMs matching the pool's
power state; on scale-in, instances are deleted per the scale-in policy and the pool refills to its maximum ready capacity.

## Create
Register the `Microsoft.StandbyPool` resource provider on the subscription first, then:
```bash
az standby-vm-pool create -g <rg> -n sp-web \
  --vmss-id $(az vmss show -g <rg> -n vmss-web --query id -o tsv) \
  --max-ready-capacity 20 --min-ready-capacity 5 --vm-state Deallocated
az standby-vm-pool status --resource-group <rg> --name sp-web
```
The `az standby-vm-pool` commands come from a CLI extension (installs on first use; reference states Azure CLI 2.75.0
or higher). `--vm-state` accepts `Deallocated`, `Hibernated` or `Running`.
- **Minimum ready capacity**: user-defined floor, default zero for a new pool; the pool creates a replacement whenever
  a VM leaves it and the count drops below the minimum.
- **Maximum ready capacity**: tied to scale set instance count (the pool size counts instances in the scale set too):
  with a maximum of 20 and 10 instances in the scale set, the pool size is 10.
- **Deallocated** VMs are shut down and keep disks, NICs and static IPs, and are started automatically when moved into
  the scale set. **Running** VMs are ready for traffic immediately and are recommended for strict latency and
  reliability needs, but incur compute, networking and storage costs. Ephemeral OS disks don't support deallocated.

## Permissions
The standby pool resource provider needs permissions to work; follow the permissions section of the overview page
(role assignments for the resource provider) or creation and refill fail.

## Sizing
- Set ready capacity to the burst you need in the first minutes; check autoscale history for peak steps.

## Gotchas
- Flexible orchestration only; Uniform is not supported. Attaching multiple standby pools to one scale set is not supported.
- Running-state pools cost more while idle; weigh against the latency requirement.

## Verify
- [ ] Scale-out test: time from autoscale action to healthy instance drops versus baseline; pool refills afterwards.

## Checked
2026-10-27. Confirmed against Learn "Standby pools overview" (states, min/max ready capacity semantics, limitations),
"Create a standby pool" (updated 2026-05-19) and the az standby-vm-pool CLI reference (create flags, `--vm-state` enum,
`status` command, extension note). Fixed: `az standby-vm-pool status show` is `az standby-vm-pool status`; the old
example showed `--max-ready-capacity 10` semantics loosely. Removed: the named permission roles for the resource
provider (not on fetched pages), predictive autoscale advice, "start takes about a minute", the model-staleness
claim and region-availability note.
Method: documentation only; no commands were run.
