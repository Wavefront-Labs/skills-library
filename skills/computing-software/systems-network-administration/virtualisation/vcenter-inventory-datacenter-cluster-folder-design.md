---
id: computing-software.systems-network-administration.virtualisation.vcenter-inventory-datacenter-cluster-folder-design
name: vcenter-inventory-datacenter-cluster-folder-design
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcenter-inventory, vcenter-folders, vsphere-inventory, permissions, vmware, vcenter, vsphere]
level: practitioner
status: draft
description: "Design the vCenter inventory: datacenters, clusters, host/VM/storage/network folders and naming so permissions, DRS, tags and automation stay simple."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management-8-0/organizing-your-inventory-host-management.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security-8-0/vsphere-permissions-and-user-management-tasks/best-practices-for-roles-and-permissions.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vCenter inventory design

**Goal:** an inventory where permissions, policies and scripts follow the structure instead of fighting it.

## Hierarchy rules
- **Datacenter** is a boundary: vMotion, vDS, datastores and networks are scoped to it (cross-datacenter needs cross-vCenter style moves). Use one per physical site; do not use datacenters as departments.
- **Cluster** groups identical hosts sharing storage/network; DRS/HA/EVC/vLCM image are per cluster. Keep hosts in a cluster the same model/CPU generation.
- **Folders** exist in four separate trees: Hosts and Clusters, VMs and Templates, Storage, Networking. Permissions and tags are applied to folders.

## Folder pattern
```
DC-SYD
 VMs and Templates
   Prod / App-A, App-B
   NonProd / Dev, Test
   Infrastructure / vCenter, DNS, Backup
   Templates
```
- Grant roles on folders (Prod -> AppTeam-A-Operators) with propagate on; avoid per-VM permissions.
- Keep templates in their own folder with a read-only role for consumers.

## Naming
`<site>-<role>-<nn>` for hosts and clusters (`syd-prod-cl01`, `syd-esx-014.example.com`), lower-case DNS FQDN for hosts. Do not encode IPs or owners in names; use tags/custom attributes for owner, cost centre, backup tier.

## Automation
```powershell
New-Folder -Name Prod -Location (Get-Folder vm -Location (Get-Datacenter DC-SYD))
Get-Folder Prod | New-Folder -Name App-A
Move-VM -VM app-a-* -InventoryLocation (Get-Folder App-A)
```
Scripts that target folders/tags survive cluster renames; scripts targeting names do not.

## Gotchas
- Moving a VM between VM folders does not move it between clusters (VM folders are logical).
- A permission on the vCenter root with propagate gives access to everything, including future objects.
- Too many nested resource pools as "folders" breaks share maths; use folders for organisation, resource pools for resources.

## Verify
Every VM lives in a non-root folder; `Get-VIPermission` shows grants on folders and clusters only; new VMs land in the right folder via templates/automation.
