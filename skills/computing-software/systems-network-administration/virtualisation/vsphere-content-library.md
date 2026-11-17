---
id: computing-software.systems-network-administration.virtualisation.vsphere-content-library
name: vsphere-content-library
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [content-library, subscribed-library, published-library, vm-template, ovf, iso, template-versioning, vsphere-vm-administration, vmware, vsphere]
level: practitioner
status: draft
description: "Run vSphere content libraries: local vs published/subscribed, VM templates vs OVF items, check-out/check-in versioning, on-demand sync, and storage placement."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSphere content libraries

**Goal:** one source of truth for templates and ISOs, replicated to every vCenter and site,
with versions you can roll back.

## Library types
- **Local library**: on one vCenter; optionally **published** (HTTPS, optional password).
- **Subscribed library**: points at a published library URL (another vCenter, or any web
  server hosting a `lib.json`). Sync **immediately** (copies everything) or **on demand**
  (metadata only; content downloaded when first used: saves space at remote sites, slows
  first deployment).

## Item types
| Type | Notes |
|---|---|
| VM template (vSphere 6.7U1+) | Native template stored in the library; supports **check out / check in** versioning; does not sync to subscribed libraries as VM templates across different vCenters (converted to OVF in sync in some versions; check) |
| OVF template | Portable; syncs everywhere; deploy with customisation |
| ISO and other files | Install media, scripts |

## Template versioning workflow
1. Library → VM template → **Check out** to a VM.
2. Patch/modify the VM, then **Check in** with a change note. Previous version is kept
   (one previous by default) and can be reverted.
3. Deployments always use the latest checked-in version.

## Automation
```powershell
Get-ContentLibrary
Get-ContentLibraryItem -ContentLibrary Templates -Name win2022-std
New-VM -Name app02 -ContentLibraryItem (Get-ContentLibraryItem win2022-std) -VMHost esx01 -Datastore ds01
```

## Gotchas
- Backing datastore of a library fills up fast with versions and ISOs; size it and
  monitor it like any datastore.
- Published library password changes break subscribers silently until next sync.
- A subscribed library is read-only: patching the template must happen on the publisher.
- Library sync uses vCenter-to-vCenter HTTPS; large sites benefit from on-demand.

## Verify
Subscribed libraries show "Last sync" recent and item counts matching the publisher;
a test deploy from each site completes; the template's version history shows a check-in
for the latest monthly patch.
