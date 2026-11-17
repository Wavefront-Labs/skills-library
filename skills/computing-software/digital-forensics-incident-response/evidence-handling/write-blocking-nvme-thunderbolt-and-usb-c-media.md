---
id: computing-software.digital-forensics-incident-response.evidence-handling.write-blocking-nvme-thunderbolt-and-usb-c-media
name: write-blocking-nvme-thunderbolt-and-usb-c-media
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [nvme-write-blocker, write-blocking, nvme, thunderbolt, usb-c, dfir]
level: advanced
status: draft
description: "Write-block NVMe, Thunderbolt and USB-C media: PCIe/NVMe hardware blockers and adapters, validating them, Linux software blocking, and when soldered storage forces other methods."
sources: ["https://www.cru-inc.com/products/wiebetech/", "https://www.opentext.com/products/tableau-forensic-hardware", "https://github.com/msuhanov/Linux-write-blocker"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write-blocking NVMe, Thunderbolt and USB-C media

Classic SATA/IDE blockers do not cover modern media. NVMe drives speak PCIe, many laptops solder storage to the board, and USB-C/Thunderbolt enclosures may bridge NVMe over USB or tunnel PCIe directly.

## Hardware options
- **PCIe/NVMe forensic bridges** (e.g. Tableau TX1/TD4 with NVMe/PCIe adapter, WiebeTech/CRU NVMe-capable blockers) accept M.2 NVMe directly. Check form factor (M.2 2230/2242/2280, U.2) and keying (M key); adapters exist for proprietary Apple and Microsoft Surface SSDs.
- **USB-C to NVMe** bridge enclosures are not write blockers; put a USB write blocker between the enclosure and the workstation, or better, use a native NVMe blocker.
- **Thunderbolt** external drives: Thunderbolt tunnels PCIe and gives DMA; use a blocker that supports the device natively, or remove the internal drive and attach it to an NVMe blocker.

## Validation
Test each blocker with the specific adapter before casework: attach a test NVMe drive, attempt writes (create partition, `dd` to a sector, mount read-write), confirm all fail, and confirm the hash before and after is unchanged. Record firmware versions. NIST CFTT hardware write-block reports list tested devices; they do not cover every adapter combination.

## Software blocking (Linux)
```bash
blockdev --setro /dev/nvme0n1   # set before any partition probing
blockdev --getro /dev/nvme0n1   # expect 1
```
Disable automount in the forensic boot environment and set read-only before partition scanning; the Linux-write-blocker kernel patch makes new block devices read-only by default. Software blocking is weaker than hardware: document it and validate on your build.

## When you cannot remove the drive
- Soldered NVMe (many MacBooks, ultrabooks): image via target mode (Apple Silicon "share disk" / DFU-based methods), a forensic boot USB with read-only policies, or logical acquisition on the live system.
- Encrypted with hardware-bound keys (T2/Apple Silicon, TPM-only BitLocker): removal gives ciphertext; live or in-situ acquisition is required.

## Gotchas
- NVMe drives perform background garbage collection and TRIM on their own when powered; blocking host writes does not stop internal controller activity, so hashes can differ between reads of deleted areas.
- High-capacity NVMe through a USB 3 blocker is slow; budget time or use a PCIe blocker.

## Verify
Pre- and post-acquisition hashes of the test drive match through the exact blocker plus adapter chain used, and the blocker model, firmware and validation date appear in the collection log.
