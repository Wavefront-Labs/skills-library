---
id: computing-software.cloud-infrastructure-engineering.azure.disk-access-and-network-access-policy-for-disk-export
name: disk-access-and-network-access-policy-for-disk-export
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-disks, disk-access, network-access-policy, disk-export-sas, private-link, data-exfiltration]
level: advanced
status: docs-checked
description: "Stop managed disk and snapshot exfiltration via SAS: network access policy (AllowPrivate/DenyAll), disk access resources with private endpoints, and policy enforcement."
sources: ["https://learn.microsoft.com/azure/virtual-machines/disks-enable-private-links-for-import-export-portal", "https://learn.microsoft.com/azure/virtual-machines/disks-restrict-import-export-overview", "https://learn.microsoft.com/cli/azure/disk-access", "https://learn.microsoft.com/cli/azure/disk", "https://learn.microsoft.com/azure/virtual-machines/policy-reference"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk access and network access policy

**Goal:** a person with disk read rights can't generate a public SAS and download your database server's disk.

## The risk
`az disk grant-access` (or snapshot grant-access) creates a SAS URL to the whole VHD, downloadable from anywhere
by default. Same path is used for direct upload (import).

## Options per disk/snapshot
| networkAccessPolicy | Effect |
|---|---|
| AllowAll | Export/import SAS works from any network |
| AllowPrivate | Only through a **disk access** resource's private endpoint |
| DenyAll | No export/import at all |
Also `publicNetworkAccess: Disabled` on the disk.

## Private export setup
```bash
az disk-access create -g rg -n da-prod -l westeurope
az network private-endpoint create -g rg -n pe-da-prod --vnet-name vnet-mgmt --subnet snet-pe \
  --private-connection-resource-id $(az disk-access show -g rg -n da-prod --query id -o tsv) \
  --group-id disks --connection-name da-prod
az disk update -g rg -n vm01-osdisk --network-access-policy AllowPrivate \
  --disk-access $(az disk-access show -g rg -n da-prod --query id -o tsv) --public-network-access Disabled
```
The disk access resource must be in the same region and subscription as the disk, and one disk access resource handles at most 100 simultaneous disk or snapshot imports/exports.

## Govern
- Built-in policies: "Managed disks should disable public network access" (Audit, Deny, Disabled) and "Configure managed disks to disable public network access" (Modify, Disabled).
- RBAC: a custom role without the `beginGetAccess` and `endGetAccess` actions for disks and snapshots cannot import or export; remove them from broad custom roles.
- Alert on `Microsoft.Compute/disks/beginGetAccess/action` and snapshot equivalents in the activity log.

## Gotchas
- Private Link only affects import and export, not a VM's access to its attached disks.
- You can't upload to a disk with both a disk access resource and a disk encryption set.
- Test tools that export via SAS before enforcing DenyAll.

## Verify
- [ ] `az disk grant-access` from outside the VNet yields a SAS that fails to download; ARG shows no disks with AllowAll in prod.

## Checked
2026-11-01. Confirmed against Microsoft Learn disks-restrict-import-export-overview, disks-enable-private-links-for-import-export-portal, az disk CLI reference (--network-access-policy AllowAll/AllowPrivate/DenyAll, --public-network-access, --disk-access) and the Compute policy reference (both built-in policies). Removed: AllowAll-default claim, private DNS zone name, snapshot inheritance, disk-encryption-set policy, backup/ASR/Image Builder and cost claims (not stated).
Method: documentation only; no commands were run.
