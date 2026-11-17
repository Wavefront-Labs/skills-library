---
id: computing-software.systems-network-administration.virtualisation.vsphere-tags-and-custom-attributes
name: vsphere-tags-and-custom-attributes
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-tags, custom-attributes, tagging, powercli, vmware, vsphere]
level: practitioner
status: draft
description: "Design and manage vSphere tag categories, tags and custom attributes with PowerCLI, and use them for backup scope, storage policies and reporting."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management-8-0/vsphere-tags-and-attributes-host-management.html
  - https://developer.broadcom.com/powercli/latest/vmware.vimautomation.core/commands/new-tagassignment
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vSphere tags and custom attributes

**Goal:** consistent, queryable metadata on inventory objects that automation and backup tools can rely on.

## Tags vs custom attributes
| | Tags | Custom attributes |
|---|---|---|
| Structure | Category (cardinality, object types) -> tag | Key/value per object |
| Scope | Replicated across Enhanced Linked Mode | Per vCenter |
| Used by | SPBM tag-based placement, backup job scope, NSX, Aria | Notes fields, backup "last backup" stamps |

## Create and assign
```powershell
New-TagCategory -Name Environment -Cardinality Single -EntityType VirtualMachine
New-Tag -Name Prod -Category Environment
New-TagCategory -Name Backup -Cardinality Multiple -EntityType VirtualMachine,Datastore
New-Tag -Name Daily -Category Backup

Get-VM -Name 'sql*' | New-TagAssignment -Tag (Get-Tag Prod -Category Environment)
Get-TagAssignment -Category Environment | Select Entity, Tag

# Custom attribute
New-CustomAttribute -Name Owner -TargetType VirtualMachine
Get-VM app01 | Set-Annotation -CustomAttribute Owner -Value 'team-payments'
```

## Design rules
- Single-cardinality categories for mutually exclusive facts (environment, tier); multiple for memberships (backup policies, applications).
- Restrict *Associable entities* so tags cannot land on the wrong object type.
- Name tags exactly as automation expects; renaming a tag breaks scripts that match by name but not tag-based backup jobs that use its ID.
- Tag permissions are global; grant *Assign or Unassign vSphere Tag* to automation accounts only.

## Gotchas
- Re-registering a VM drops its tags; export first: `Get-TagAssignment | Export-Csv tags.csv`.
- Tags live in vCenter, not on the host; a VM moved to another non-linked vCenter loses them.
- Tag queries in PowerCLI are slow on large estates; cache `Get-TagAssignment` once per run.

## Verify
`Get-VM -Tag Prod` returns the expected set; backup job scope shows the same VM count.
