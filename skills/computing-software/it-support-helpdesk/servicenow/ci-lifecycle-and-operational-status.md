---
id: computing-software.it-support-helpdesk.servicenow.ci-lifecycle-and-operational-status
name: ci-lifecycle-and-operational-status
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, ci-lifecycle, operational-status, install-status, life-cycle-stage, cmdb, asset-ci-sync]
level: practitioner
status: gated
description: "Keep ServiceNow CI lifecycle fields right: life cycle stage and status, legacy install/operational status, asset-CI sync, and what to set on repair, swap and retire."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/configuration-management/concept/ci-lifecycle-management.html"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/product/csdm-implementation/concept/csdm-life-cycle-standards.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-asset-management/page/product/asset-management/concept/c_AssetAndCISynchronization.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ci-lifecycle-and-operational-status

Stale status values make the CMDB lie: retired laptops still "In use", servers in repair
showing operational, swapped devices assigned to two people. Desk and desk-side teams
change hardware more than anyone, so they own much of this hygiene.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Fields (CSDM life cycle standard)
- **Life Cycle Stage** (`life_cycle_stage`): Ideation, Design, Build, Deploy, Operational,
  End of Life, ... plus **Life Cycle Stage Status** (`life_cycle_stage_status`) e.g.
  Operational/In Use, Operational/In Maintenance, End of Life/Retired, End of Life/Stolen.
  This pair replaces the legacy fields in current CSDM.
- Legacy and still widely used: `install_status` (Installed, In maintenance, Pending
  install, Retired, Stolen, Absent) and `operational_status` (Operational, Non-operational,
  Repair in progress, DR standby, Retired).
- Asset side (`alm_hardware`): `install_status` + `substatus` (In use, In stock/Available,
  In stock/Pending repair, Retired/Disposed). Asset-CI synchronisation copies the mapped
  values both ways according to `alm_asset_ci_state_mapping`.

## What support sets
| Event | Asset | CI |
|---|---|---|
| Device sent for repair | In stock / Pending repair (or In use, if loaner) | In maintenance / Repair in progress |
| Swap: old device returned | In stock / Pending repair or Retired | Assigned to cleared |
| New device issued | In use, Assigned to = user | Installed / Operational |
| Lost or stolen | Missing / Stolen | Stolen; link the security incident |
| Disposed with certificate | Retired / Disposed, disposal reason | Retired / End of Life Retired |

Update the asset when HAM is in use; let sync update the CI. Editing both by hand fights
the sync.

## Hygiene reports
- CIs Operational but not seen by discovery/Intune for 60 days (`last_discovered`).
- Hardware assets In use with no Assigned to, or assigned to inactive users.
- Retired CIs still referenced by open incidents or changes.

## Gotchas
- Discovery or the Intune/SCCM connector can flip a retired CI back to Installed if the
  device still reports in; wipe or delete the device in the source too.
- Retiring a CI doesn't remove its relationships; impact analysis may still show it.

## Verify
After a swap, the old and new device each show one consistent owner and status on both
asset and CI, and the hygiene reports drop the record.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
