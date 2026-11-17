---
id: computing-software.systems-network-administration.patch-management.firmware-rollback-and-dual-bank-images
name: firmware-rollback-and-dual-bank-images
category: computing-software
field: systems-network-administration
product: patch-management
tags: [firmware-rollback, dual-bank, backup-image, anti-rollback, firmware-patching, patch-management]
level: practitioner
status: draft
description: "Plan for firmware rollback: primary/backup BMC and BIOS banks, Dell/HPE/Lenovo rollback paths, network gear boot images, and anti-rollback fuses that block downgrades."
sources:
  - https://www.dell.com/support/manuals/en-us/idrac9-lifecycle-controller-v7.x-series/idrac9_7.xx_ug/rolling-back-device-firmware
  - https://support.hpe.com/hpesc/public/docDisplay?docId=sd00002007en_us
  - https://pubs.lenovo.com/xcc2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firmware rollback and dual-bank images

Firmware updates are the patches most likely to brick a device and the hardest to undo. Know the rollback path before flashing.

## Dual-bank (A/B) firmware
Many components keep two images: running and backup/previous.
- **Dell iDRAC/Lifecycle Controller**: keeps previous version for BIOS, iDRAC, NICs, RAID; Maintenance > System Update > Rollback (or `racadm rollback` / Redfish `SimpleUpdate` with the rollback image).
- **HPE iLO 5/6**: iLO firmware has primary/backup; "Recovery set" in iLO Repository can restore a known-good set; System ROM has a redundant/backup ROM selectable at boot (RBSU).
- **Lenovo XCC**: primary and backup XCC banks; "Activate backup" in XCC UI; UEFI has primary/backup images.
- **Network gear**: keep previous image on flash and set `boot system` fallback (Cisco `boot system flash:old.bin` as second entry), Junos `request system software rollback`, FortiGate alternate firmware partition (`execute set-next-reboot secondary`).

## Procedure
1. Before update: record current versions, confirm backup bank holds the current good version (some updates overwrite backup first).
2. Flash one device; verify boot and function.
3. Only then roll out; backup bank now holds old version, primary holds new.
4. If bad: rollback via the mechanism above; if the device does not boot, BMC recovery mode / serial console / vendor recovery jumper.

## Anti-rollback
- Security fixes may increment a **security version number (SVN)** or blow eFuses (e.g. some Intel ME/CSME, TPM, Apple/phone SoCs, HPE iLO "downgrade policy", Cisco secure boot images). Downgrade becomes impossible or blocked by policy.
- Release notes state "cannot downgrade below version X"; treat those updates as one-way and test longer.

## Gotchas
- Rolling back BMC firmware does not roll back BIOS settings changed by the new version.
- Dependency chains: new NIC firmware may require new driver; rolling firmware back without the driver breaks networking.

## Verify
Runbook per device family with rollback steps tested once on a lab unit; pre-change version records exist in the change.
