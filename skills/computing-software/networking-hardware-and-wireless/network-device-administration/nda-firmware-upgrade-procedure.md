---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-firmware-upgrade-procedure
name: nda-firmware-upgrade-procedure
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [network-firmware-upgrade, image-verification, upgrade-rollback-plan, nda-lifecycle]
level: practitioner
status: draft
description: "Plan device firmware upgrades: choose a vendor-recommended release, verify image hashes, stage, schedule, upgrade and roll back."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
  - https://help.ui.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firmware upgrade procedure

1. Pick the vendor-recommended or gold release; read release notes and known issues; check upgrade path (some jumps require interim versions).
2. Download the image and verify checksum/signature; check free flash.
3. Back up config and record `show version`, interfaces and routing state.
4. Stage the image; upgrade one member of each redundant pair at a time, in a window, with console access.
5. Verify state: interfaces, adjacencies, MAC/ARP counts, licences.
6. Keep the previous image to roll back; do not delete until stable.
- Use canary devices first. For UniFi, staged firmware rollouts and device auto-upgrade settings exist; review them.

## Verify
- [ ] Post-upgrade state matches the pre-upgrade snapshot and monitoring is clean for a defined soak period.
