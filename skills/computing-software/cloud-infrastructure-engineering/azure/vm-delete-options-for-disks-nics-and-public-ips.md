---
id: computing-software.cloud-infrastructure-engineering.azure.vm-delete-options-for-disks-nics-and-public-ips
name: vm-delete-options-for-disks-nics-and-public-ips
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, virtual-machines, delete-option, vm-delete, orphaned-resources, force-delete]
level: practitioner
status: docs-checked
description: "Stop orphaned disks, NICs and public IPs: set deleteOption at VM create or update, force delete, and find leftovers with Resource Graph."
sources: ["https://learn.microsoft.com/azure/virtual-machines/delete", "https://learn.microsoft.com/cli/azure/vm#az-vm-create", "https://learn.microsoft.com/azure/virtual-machines/windows/find-unattached-disks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM delete options

**Goal:** deleting a VM removes everything that belongs only to it - or deliberately keeps what you want.

## At creation
```bash
az vm create -g rg -n vm01 --image Ubuntu2204 \
  --os-disk-delete-option Delete --data-disk-delete-option Delete --nic-delete-option Delete
```
Each option is `Delete` (removed with the VM) or `Detach` (left in Azure for reuse; detached resources keep incurring charges).
REST/ARM: `storageProfile.dataDisks[].deleteOption` and `networkProfile.networkInterfaces[].properties.deleteOption`
(api-version 2021-03-01 or newer). The CLI and PowerShell default detaches the OS disk. In the portal the new OS disk is
set to delete with the VM by default (an existing OS disk detaches), and a checkbox deletes the public IP and NIC.

## Existing VMs
Learn documents changing the delete behaviour of an existing VM through the portal, PowerShell and a REST update
(api-version 2021-03-01 or newer) that sets `deleteOption` on the NIC, OS disk and data disks. Follow the "Update the
delete behavior on an existing VM" section of the delete article.

## Deleting
```bash
az vm delete -g rg -n vm01 --yes
az vm delete -g rg -n vm01 --yes --force-deletion true    # reduces delete latency, frees attached resources immediately
```
Force delete suits VMs that do not need a graceful shutdown.

## Find orphans
By default deleting a VM does not delete its disks. The Learn article on unattached disks finds managed disks through the
`ManagedBy` property (empty when not attached to a VM) and unmanaged disks through the page blob `LeaseStatus`; review the
list before deleting. Detached disks keep incurring charges.

## Gotchas
- Keep the OS disk (Detach) deliberately when you might rebuild from it or for forensics.

## Verify
- [ ] Test VM delete leaves no disk, NIC or public IP behind unless you chose Detach.

## Checked
2026-10-28. Confirmed in Learn `virtual-machines/delete` and `find-unattached-disks` and the `az vm create`/`az vm delete` references: Delete
versus Detach, the three create-time delete-option flags, CLI/PowerShell OS disk default, portal defaults, api-version
2021-03-01, force delete flag, ManagedBy and LeaseStatus detection. Removed: the public IP property path, `az vm update --set`
examples, the Resource Graph orphan queries (diskState and related properties not confirmed), the shared disk, snapshot/NSG and
Premium full-price claims.
Method: documentation only; no commands were run.
