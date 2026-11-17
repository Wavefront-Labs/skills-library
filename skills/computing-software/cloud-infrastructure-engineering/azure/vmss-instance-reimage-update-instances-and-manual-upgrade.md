---
id: computing-software.cloud-infrastructure-engineering.azure.vmss-instance-reimage-update-instances-and-manual-upgrade
name: vmss-instance-reimage-update-instances-and-manual-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vmss, reimage, update-instances, manual-upgrade, latest-model, instance-operations]
level: practitioner
status: gated
description: "Operate scale set instances: check latestModelApplied, roll out model changes with update-instances under Manual policy, reimage, restart, and delete specific instances."
sources: ["https://learn.microsoft.com/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-upgrade-policy", "https://learn.microsoft.com/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-reimage-virtual-machine", "https://learn.microsoft.com/cli/azure/vmss"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VMSS instance operations

**Goal:** apply scale set model changes to instances on your terms, and fix bad instances without touching healthy ones.

## Which instances are behind the model?
```bash
az vmss list-instances -g rg -n vmss-web \
  --query "[].{id:instanceId,name:name,latest:latestModelApplied,state:provisioningState,zone:zones[0]}" -o table
```
`latestModelApplied=false` means the instance is behind the scale set model (gated: unconfirmed, source is paywalled or blocked).

## Manual upgrade policy: roll out yourself
```bash
az vmss update -g rg -n vmss-web --set virtualMachineProfile.storageProfile.imageReference.version=1.4.0
az vmss update-instances -g rg -n vmss-web --instance-ids 0 1          # canary
# verify health, then the rest in batches
az vmss update-instances -g rg -n vmss-web --instance-ids 2 3 4
az vmss update-instances -g rg -n vmss-web --instance-ids "*"
```
The available upgrade policy modes are automatic, manual and rolling; with Manual you choose when instances are updated.

## Reimage
```bash
az vmss reimage -g rg -n vmss-web --instance-ids 3        # replaces the OS disk with a new one
```
Use for a corrupted or drifted instance, or to apply OS, data disk profile or custom data changes. With an ephemeral OS disk the instance returns to its initial state and local data is lost; with non-ephemeral disks, retention of the old OS disk depends on the scale set settings.

## Other instance ops
```bash
az vmss restart -g rg -n vmss-web --instance-ids 3
az vmss deallocate -g rg -n vmss-web --instance-ids 3
az vmss delete-instances -g rg -n vmss-web --instance-ids 3      # capacity decreases by 1
az vmss get-instance-view -g rg -n vmss-web --instance-id 3
```

## Gotchas
- Instance Protection is the documented control for keeping chosen instances from being upgraded with the rest.
- Under Manual policy nothing happens automatically to existing instances when the model changes.

## Verify
- [ ] All instances show `latestModelApplied: true`; app health extension reports healthy after each batch.

## Checked
2026-10-28. Confirmed on the upgrade-policy and reimage pages: modes automatic/manual/rolling, Manual leaves existing VMs untouched, Instance Protection, reimage replaces the OS disk and applies OS/data disk profile/custom data changes, ephemeral OS disk local data is lost. check_commands confirmed every `az vmss` command and flag. Gated: the `latestModelApplied` meaning (property not on fetched pages). Removed: data-disks-kept claim, Automatic-at-once advice, Flexible orchestration note, autoscale mixed-fleet and extension re-run claims.
Method: documentation only; no commands were run.
