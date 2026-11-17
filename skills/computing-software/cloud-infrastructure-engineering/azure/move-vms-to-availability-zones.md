---
id: computing-software.cloud-infrastructure-engineering.azure.move-vms-to-availability-zones
name: move-vms-to-availability-zones
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, virtual-machines, zone-migration, move-to-zone, availability-zones, resource-mover]
level: advanced
status: docs-checked
description: "Move regional (non-zonal) VMs into availability zones: Resource Mover / zonal move, the manual snapshot-and-rebuild path, public IP and load balancer prerequisites."
sources: ["https://learn.microsoft.com/azure/virtual-machines/move-virtual-machines-regional-zonal-portal", "https://learn.microsoft.com/azure/reliability/migrate-vm", "https://learn.microsoft.com/azure/resource-mover/move-region-availability-zone"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Move VMs into availability zones

**Goal:** turn VMs deployed with no zone into zonal VMs spread across zones, with a planned downtime window.

## Facts first
- The zonal move creates a copy of the VM in the target zonal configuration (new VM, new NIC, new disks; the
  source ARM IDs are not retained). The source VM is stopped, so there is brief downtime, and it stays
  stopped afterwards until you delete or reuse it.
- Standard SKU public IPs and load balancers support zonal deployment and are retained; Basic SKU ones do not
  support it and the move creates new Standard SKU ones by default.
- Plan which VMs go to zones 1/2/3 - pairs of HA nodes must land in different zones.

## Option A: portal zonal move
VM overview > **Availability + scaling > Edit**: pick the target availability zone (validation fails if the
configuration is unsupported; Azure may recommend another size), consent to the system-assigned managed
identity setup, review the properties (VM name, VNet/subnet, NSG and Standard SKU resources are retained),
then Move. Prerequisites on the Learn page: the region supports zones, size availability in the zone, Owner
on the subscription for the first move, quota, and a healthy VM. Quota approval does not guarantee zone
capacity. Afterwards re-check extensions, RBAC, backup and disaster recovery settings. The move uses a move
collection that you can delete later; PowerShell and CLI (`az resource-mover`) routes also exist.

## Option B: manual rebuild
```bash
az vm deallocate -g rg -n app01
az snapshot create -g rg -n app01-os-snap --source app01-osdisk --incremental true
az disk create -g rg -n app01-os-z2 --source app01-os-snap --zone 2 --sku Premium_LRS
# repeat for data disks, then:
az vm delete -g rg -n app01 --yes          # keep NIC (deleteOption Detach)
az vm create -g rg -n app01 --attach-os-disk app01-os-z2 --os-type Linux --zone 2 --nics app01-nic \
  --size Standard_D4s_v5 --attach-data-disks app01-data0-z2
```
Re-apply extensions, managed identity role assignments, backup protection and diagnostics.

## Prerequisites checklist
- Public IP and load balancer: Standard SKU, or accept the new Standard resources the move creates.
- Capacity: check the size is offered in each target zone (`az vm list-skus -l westeurope --size D4s_v5 --zone`).
- Backups and monitoring: the new VM is a new resource; reconfigure protection and keep old recovery points
  until retention allows.

## Gotchas
- Encryption keys and disk encryption sets must be usable for the copies; verify before the window.

## Verify
- [ ] `az vm show --query zones` shows the target zone; application health checks pass; old disks/snapshots cleaned up after sign-off.

## Checked
2026-10-28. Confirmed against the regional-to-zonal move page (prerequisites, retained and newly created
properties, Standard versus Basic SKU behaviour, brief downtime, source VM left stopped, move collection
cleanup) and the command checker. Removed as unconfirmed: Basic retirement statement, availability set
rule, Ultra and Premium SSD v2 zonal statement, ZRS disk alternative, the manual-rebuild steps were kept only as
command examples that were not run.
Method: documentation only; no commands were run.
