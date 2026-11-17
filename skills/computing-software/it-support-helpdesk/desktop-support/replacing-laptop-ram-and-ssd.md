---
id: computing-software.it-support-helpdesk.desktop-support.replacing-laptop-ram-and-ssd
name: replacing-laptop-ram-and-ssd
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, laptop-hardware, hardware-replacement, ram-ssd-upgrade, so-dimm, m-2, nvme, sata, soldered-ram, disk-cloning, bitlocker-suspend, comptia-a-plus]
level: practitioner
status: draft
description: "Upgrade or replace laptop RAM and SSDs: identify SO-DIMM vs soldered, M.2 key and length, NVMe vs SATA, clone or reimage, and handle BitLocker and warranty rules."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.dell.com/support/manuals/"
  - "https://pcsupport.lenovo.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# replacing-laptop-ram-and-ssd

Goal: the right part, fitted first time, with the user's data and
encryption intact.

## Identify before ordering
- Service manual for the exact model (Dell/HP/Lenovo publish them by service
  tag/serial): RAM slots count, max capacity, SSD slots and supported form
  factors.
- **RAM**: SO-DIMM DDR4/DDR5 slots vs **soldered** (LPDDR — not upgradeable;
  many thin laptops). Match speed; mixed sizes run but may lose dual-channel.
  `wmic memorychip get capacity,speed,devicelocator,partnumber` or Task
  Manager → Performance → Memory (slots used).
- **SSD**: M.2 2280/2242/2230 (length in mm), key M (NVMe PCIe) vs B+M (often
  SATA). An NVMe-only slot won't run a SATA M.2 drive. Check the PCIe gen
  and single/double-sided clearance.

## Procedure
1. Ticket notes: serial, part numbers, warranty status (vendor-sealed or
   on-site warranty may require vendor fitting).
2. Suspend BitLocker: `manage-bde -protectors -disable C: -RebootCount 1`
   (hardware change alters measurements).
3. Shut down fully (Shift+Shutdown — Fast Startup isn't off), unplug,
   **disable the internal battery** in BIOS if offered (Dell "battery
   disconnect") or disconnect the battery connector first.
4. ESD strap to chassis ground; mat if available.
5. RAM: release side clips, remove at 30°, insert new at 30° until contacts
   disappear, press down to click.
6. SSD: remove screw/standoff, swap, keep the thermal pad/heat spreader.
7. Boot to BIOS — confirm detected capacity and drive.

## Data on SSD replacement
- **Reimage** (Autopilot reset / provisioning) is the standard in managed
  fleets — data lives in OneDrive. Confirm sync complete before.
- **Clone** when needed: vendor tool or Macrium/Clonezilla from old drive
  in USB-NVMe enclosure; then extend the partition (and fix recovery
  partition layout if moved).
- Old drive: becomes sensitive media — sanitise or destroy per policy.

## Gotchas
- New RAM not detected → reseat; some models require a "memory training"
  first boot (black screen for 1–2 minutes) — wait before declaring DOA.
- Intel VMD/RST: new drive isn't visible to Windows setup without the VMD
  driver.
- Ribbon cables (keyboard, battery) tear easily; lift ZIF latches first.

## Verify
BIOS and Windows show the new capacity; a memory test (Windows Memory
Diagnostic or vendor diagnostics) passes; SMART health OK; BitLocker
re-enabled (`manage-bde -status`).
