---
id: computing-software.systems-network-administration.virtualisation.vcenter-upgrade-and-vami-patching
name: vcenter-upgrade-and-vami-patching
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-upgrade, vcenter-upgrade, vami-patching, software-packages, vcsa, reduced-downtime-upgrade, upgrade-order, interoperability-matrix, vmware, vcenter, vsphere]
level: practitioner
status: docs-checked
description: "Patch and upgrade vCenter: VAMI and software-packages CLI patching, major upgrades via the installer, the vSphere upgrade order, interoperability checks and rollback snapshots."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-upgrade/upgrading-and-updating-the-vcenter-server-appliance/reduced-downtime-upgrade.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-upgrade/patching-and-updating-vcenter-server/patching-the-vcenter-server-appliance/patching-the-vcenter-server-appliance-by-using-the-appliance-shell/stage-software-packages-to-the-vcsa.html
  - https://interopmatrix.broadcom.com/Interoperability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vCenter upgrades and VAMI patching

**Goal:** keep vCenter current (it must be at least as new as every host it manages) with
a tested rollback point.

## Upgrade order (whole stack)
1. Check the **interoperability matrix**: backup software, NSX, Aria/vROps, SRM, vSAN,
   storage plug-ins and hardware vendor tools must support the target.
2. Linked products in their documented order (often: SRM/vSphere Replication and
   backup compatibility first, then NSX manager if required).
3. **vCenter** (all ELM nodes in the same window).
4. **ESXi hosts** (vLCM), then vSAN on-disk format, then **VM Tools / hardware** if needed,
   then **vDS version**.

## Patching within a release (VAMI)
- Take a file-based backup, then an **offline-consistent snapshot** (power off VCSA, or
  at least a snapshot with no memory; for ELM snapshot all nodes powered off together).
- VAMI `:5480` → Update → Check updates (online) or stage an ISO patch (offline).
- CLI alternative over SSH:
```sh
software-packages stage --url            # or --iso with the patch ISO mounted
software-packages list --staged
software-packages install --staged
```
- vCenter 8.0U2+ supports **reduced downtime upgrade**, a migration-based approach that
  reduces upgrade downtime to minutes (initially single, self-managed vCenters without
  vCenter HA or Enhanced Linked Mode; check the RDU documentation for current scope).

## Major upgrades (e.g. 7 → 8)
Run the VCSA installer → Upgrade: it deploys a new appliance with a temporary IP, copies
configuration (and optionally historical data), then shuts the old one and takes over
its identity. Keep the old VM powered off (rename it) as the rollback for a few days.

## Gotchas
- Expired certificates (STS signing, machine SSL) block upgrades; check with VDT or the
  certificate pre-checks first.
- Root password expiry on VCSA (90 days default) breaks SSH and pre-checks; reset and set
  a sensible policy.
- Upgrade pre-check failures on plugins: unregister stale solutions in MOB/extensions.
- Don't delete the snapshot until hosts, backups and integrations are validated.

## Verify
VAMI shows the new build; all services healthy; hosts connected; backup jobs and plug-ins
work; then delete the snapshot.

## Checked
2026-10-31: Confirmed `software-packages stage --iso/--url`, `list --staged` and
`install --staged` against the "Stage Software Packages" and appliance-shell patching
pages plus the vCenter 8.0U2 release notes; the reduced downtime upgrade introduction in
8.0U2 against the RDU documentation and release notes; the 90-day root password expiry
against the fetched patching/release-notes pages. Removed the 72-hour snapshot figure
(operational advice, not documented).
Method: documentation only; no commands were run.
