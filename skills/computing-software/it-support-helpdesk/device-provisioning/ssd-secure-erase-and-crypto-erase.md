---
id: computing-software.it-support-helpdesk.device-provisioning.ssd-secure-erase-and-crypto-erase
name: ssd-secure-erase-and-crypto-erase
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, data-sanitization, crypto-erase, ssd-secure-erase, nvme-format, nvme-sanitize, ata-secure-erase, bios-data-wipe, nist-800-88, purge, sanitization-verification]
level: advanced
status: draft
description: "Purge SSDs correctly for reuse or resale: why overwriting fails on flash, NVMe sanitize/format and ATA secure erase, firmware data-wipe tools, crypto erase, and verification."
sources:
  - "https://csrc.nist.gov/pubs/sp/800/88/r1/final"
  - "https://nvmexpress.org/specifications/"
  - "https://www.dell.com/support/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ssd-secure-erase-and-crypto-erase

Goal: data on a flash drive is unrecoverable before the device is
redeployed outside its trust boundary, sold or recycled.

## Why not just overwrite
SSDs remap writes (wear levelling, over-provisioned spare blocks), so a
multi-pass overwrite of the visible LBAs leaves old data in blocks the host
can't address. NIST SP 800-88 classes overwriting as **Clear** at best for
flash; reuse outside the organisation needs **Purge**.

## Purge methods (use the drive's own controller)
1. **Firmware/BIOS data wipe** — easiest at scale: Dell "Data Wipe" (BIOS
   Maintenance → Data Wipe on next boot), HP "Secure Erase" in HP Sure Admin /
   BIOS, Lenovo ThinkShield "Secure Wipe". Issue the drive-native sanitize
   commands for the internal drive.
2. **NVMe** from a Linux live USB (`nvme-cli`):
   ```bash
   nvme id-ctrl /dev/nvme0 -H | grep -iE "sanitize|crypto|format"   # what it supports
   nvme sanitize /dev/nvme0 -a 2        # block erase (sanact=2); 4 = crypto erase
   nvme sanitize-log /dev/nvme0         # progress / status
   nvme format /dev/nvme0n1 -s 2        # format with crypto erase (ses=2) if sanitize unsupported
   ```
3. **SATA SSD**: ATA Secure Erase / Enhanced Secure Erase via `hdparm`
   (drive must not be "frozen" — suspend/resume the machine to unfreeze),
   or `hdparm --sanitize-block-erase`.
4. **Crypto erase**: drives that always encrypt (SEDs, Opal) destroy the
   media encryption key — instant. BitLocker'd drives: deleting the volume
   and keys is good extra protection but is not a NIST purge on its own
   unless the drive itself crypto-erases.

## Record and verify
- Log per device: asset tag, serial (of the drive), method, tool/version,
  date, operator, verification result — this is the sanitisation record
  required for ITAD and audits.
- Verify: sample read of the drive shows zeros/pattern (`hexdump -C
  /dev/nvme0n1 | head`), or the tool's sanitize status reports success.

## When to destroy instead
Drive failed (can't run commands), highly sensitive data per policy, or no
supported purge command → physical **Destroy** (shred/disintegrate to the
particle size the classification requires) via certified vendor.

## Gotchas
- USB enclosures block sanitize/secure erase commands — connect natively.
- Some cheap SSDs report success without erasing; sample-verify.
- Windows "Reset this PC → Clean the drive" is overwrite-based, a Clear at
  most.

## Verify
Sanitize log shows completed without error, a read sample shows no prior
data, and the device record holds the sanitisation entry.
