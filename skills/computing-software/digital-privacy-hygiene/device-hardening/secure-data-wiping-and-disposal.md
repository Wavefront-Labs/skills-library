---
id: computing-software.digital-privacy-hygiene.device-hardening.secure-data-wiping-and-disposal
name: secure-data-wiping-and-disposal
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, secure-erase, data-wiping, nist-800-88, ssd-trim, ata-secure-erase, crypto-erase, factory-reset, degaussing, physical-destruction, dban, data-sanitization, resale, disposal, hdd-wipe, ssd-wipe, chromebook-powerwash]
level: practitioner
status: draft
description: "Wipe a drive or device before resale, trade-in, return or disposal so data can't be recovered, and know why old overwrite-based methods fail on SSDs."
sources:
  - "https://csrc.nist.gov/pubs/sp/800/88/r1/final"
  - "https://support.apple.com/guide/security/erasing-content-settings-sec6dbc12256/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure data wiping and disposal

**Goal:** when a drive or device leaves your control — sold, traded in, returned
under lease, recycled, or handed to e-waste — nothing recoverable leaves with it,
using the method that actually matches the storage technology.

## 1. Why "format" or "delete" isn't enough
A quick format or moving files to the recycle bin/trash only removes the
filesystem's pointers to the data; the underlying bits stay on the media until
overwritten, and commodity recovery tools read them back trivially. This is true
for mechanical HDDs and, differently, for SSDs/flash/phones.

## 2. Mechanical hard disk drives (HDD)
- **Overwrite-based wipe** works reliably here because each logical block maps to
  a physical location you can actually overwrite. Use a full-disk pass: `DBAN`
  (free, boots from USB, single-pass is adequate per NIST 800-88 for modern
  drives — the old "7-pass" folklore is unnecessary and mostly wastes time), or
  the ATA **Secure Erase** command built into most drive firmware (accessible via
  `hdparm --security-erase` on Linux, or a vendor tool) for a faster firmware-level
  wipe.
- **Degaussing** (industrial magnetic erasure) and **physical destruction**
  (shredding, drilling through the platters) are the NIST "Purge"/"Destroy" tiers
  for drives leaving an organisation's custody entirely — overkill for a personal
  drive being resold, appropriate for regulated or highly sensitive data.

## 3. SSDs and flash storage — overwriting does not reliably work
- SSD controllers use **wear leveling**: a logical block address you "overwrite"
  may get written to a *different* physical cell, leaving the old data intact in
  a cell now marked spare/reserved. A full-disk overwrite pass that looks complete
  from the OS's view can leave recoverable fragments in over-provisioned or
  reserved flash blocks.
- The method that actually works: **ATA Secure Erase / NVMe Format with
  Secure Erase, or the vendor's own secure-erase utility**, which instructs the
  controller to purge mapping tables and reset all cells at the firmware level —
  this is the NIST 800-88 "Purge" method for SSDs, not an OS-level overwrite tool.
- **Crypto-erase**: if the drive was **whole-disk encrypted from first use**
  (BitLocker, FileVault, LUKS, or a self-encrypting drive), destroying the
  encryption key makes all data permanently unreadable instantly — this is the
  fastest and most reliable method and is why enabling encryption from day one
  (see `computing-software.digital-privacy-hygiene.device-hardening.personal-device-hardening-checklist`)
  pays off at disposal time too. If encryption was added after data already
  existed unencrypted, old plaintext may remain in unallocated/reserved space —
  crypto-erase alone doesn't fix that; still run a firmware secure erase.

## 4. Phones and tablets
- Modern iPhones/iPads and Android devices (Android 10+) encrypt storage by
  default once a screen lock is set. **Settings → Erase All Content and Settings**
  (iOS) or **Factory data reset** (Android) destroys the on-device encryption key
  as part of the process — this is a genuine crypto-erase, not a cosmetic reset,
  *provided the device was encrypted first* (it is, by default, on any device
  from the last several years). Sign out of iCloud/Google account **before**
  wiping to release Activation Lock / Factory Reset Protection, or the next owner
  (or you, if you wipe and then can't re-add the account) gets a bricked device.
- ChromeOS: **Powerwash** similarly resets and is adequate for a device that was
  encrypted (default).

## 5. What NIST 800-88 actually says, briefly
Three tiers by sensitivity and destination: **Clear** (single-pass overwrite or
reset, fine for low-sensitivity reuse within your control), **Purge** (ATA Secure
Erase, crypto-erase, or degaussing — for media leaving your control), **Destroy**
(physical destruction — for the most sensitive data or media that can't be
verified wiped). Match the tier to where the device is actually going, not to
habit.

## Gotchas
- Running DBAN or a similar overwrite-only tool on an SSD and considering it done
  is the most common mistake here — check the media type first.
- A "factory reset" on an *unencrypted* older Android phone is much weaker than
  on a modern one — verify encryption was on before relying on reset alone.
- Cloud-synced data (photos, messages, backups) isn't touched by wiping the
  device at all — separately sign out and review what's backed up.

## Verify
- [ ] Media type identified (HDD vs SSD vs phone flash) before choosing a method.
- [ ] HDD: DBAN single-pass or ATA Secure Erase run and completed without error.
- [ ] SSD: vendor/firmware Secure Erase or confirmed crypto-erase used, not a plain
      overwrite tool.
- [ ] Phone: account signed out and Activation Lock/FRP cleared before or during
      the reset.
- [ ] For anything leaving organisational custody, the method matches the NIST
      800-88 tier for its sensitivity.
