---
id: computing-software.digital-forensics-incident-response.evidence-handling.using-hardware-write-blockers
name: using-hardware-write-blockers
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [hardware-write-blocker, write-blocker, tableau, forensic-imaging, dfir]
level: practitioner
status: draft
description: "Use hardware write blockers (Tableau, WiebeTech) correctly: connection order, SATA, USB and NVMe bridges, HPA/DCO detection, and documenting the blocker used."
sources: ["https://www.nist.gov/itl/ssd/software-quality-group/computer-forensics-tool-testing-program-cftt/cftt-technical/hardware", "https://www.opentext.com/products/tableau-forensic-hardware"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using hardware write blockers

**Goal:** read a suspect drive without any write reaching it, while capturing the full
addressable area.

## Connection procedure
1. Photograph the drive label (model, serial, capacity).
2. Connect drive to the **blocker's device side** first, then power the blocker, then
   connect the **host side** (USB/Thunderbolt/FireWire) to the forensic workstation. Some
   models require this order to initialise correctly.
3. Confirm the blocker shows **write-blocked** mode (LED/display) and detects the drive
   (model, serial, capacity, HPA/DCO status on Tableau display or via Tableau Firmware
   Update/Forensic Bridge utility).
4. Image with your tool; the OS sees the device read-only.

## Interfaces
- SATA/IDE/SAS: Tableau T35u, T356789iu; WiebeTech UltraDock.
- PCIe/NVMe/M.2: Tableau TX1 imager or T7u with NVMe adapter; some proprietary SSDs
  (older Apple blades) need specific adapters.
- USB devices: USB write blocker (T8u).
- Soldered storage (modern MacBooks, many ultrabooks, eMMC) cannot be removed: use live
  logical acquisition, target disk mode/share disk mode via a blocker, or vendor tools.

## HPA and DCO
Host Protected Area and Device Configuration Overlay hide sectors from the OS. Some
blockers report and can temporarily remove HPA for imaging; check `hdparm -N /dev/sdX`
on Linux (read-only query). Document any hidden area and how it was handled.

## Document
Blocker make/model, serial, firmware version, mode, and validation reference in the
acquisition notes.

## Gotchas
- A blocker in the wrong mode (read/write for drive wiping) looks the same unless you check.
- Encrypted self-encrypting drives (OPAL) show ciphertext unless unlocked on the host.

## Verify
Hash the source through the blocker before and after imaging; values match and the
blocker log shows no write commands passed.
