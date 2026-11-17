---
id: computing-software.it-support-helpdesk.device-provisioning.disk-overwrite-and-copier-drive-sanitisation
name: disk-overwrite-and-copier-drive-sanitisation
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, disk-overwrite, copier-hard-drive, nist-800-88, data-sanitization, mfp-security, clear-purge]
level: practitioner
status: draft
description: "Sanitise HDDs by overwriting per NIST SP 800-88 Clear, and handle copier and MFP internal drives at lease return or disposal so scanned and printed data doesn't leave."
sources:
  - "https://csrc.nist.gov/pubs/sp/800/88/r1/final"
  - "https://www.ftc.gov/business-guidance/resources/digital-copier-data-security-guide-businesses"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cipher"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# disk-overwrite-and-copier-drive-sanitisation

## HDD overwrite (Clear)
- NIST SP 800-88: **Clear** = overwrite user-addressable storage (protects against simple
  recovery); **Purge** = firmware secure erase/crypto erase or degauss (lab-level
  recovery); **Destroy** = physical.
- For magnetic HDDs, a single full overwrite pass is sufficient for Clear; multi-pass
  schemes (DoD 5220.22-M 3/7-pass) add time, not meaningful security on modern drives.
- Tools: vendor/ITAD tools that also write a report (Blancco, KillDisk), `nwipe`
  (open source, from DBAN successor), Linux `dd if=/dev/zero of=/dev/sdX bs=1M
  status=progress` (verify the device name with `lsblk` first), Windows `diskpart` >
  `clean all` (writes zeros to the whole disk).
- `cipher /w:<path>` only wipes free space on a volume, not the whole disk.
- SSDs: overwriting is unreliable (over-provisioning, remapping); use secure erase or
  crypto erase instead.
- Drives that fail during overwrite (bad sectors, won't spin): physically destroy.

## Copier / MFP drives
- Many MFPs store scans, print jobs, fax images and address books on internal HDD/SSD.
- Before lease return, resale or disposal:
  1. Use the device's built-in **data overwrite / HDD erase** feature (e.g. "Initialize
     all data", "Disk overwrite" in the admin menu); some require a security kit.
  2. Or require the lessor/vendor to provide a certificate of sanitisation, or remove
     and keep/destroy the drive (negotiate in the lease contract up front).
  3. Clear address books, stored credentials (SMTP, LDAP, scan-to-folder accounts) and
     rotate those service account passwords.
- During use: enable immediate image overwrite and storage encryption features where
  available.

## Records
For every device: serial, method (Clear/Purge/Destroy), tool and version, operator,
date, verification result. Keep with the asset record; disposal certificates from ITAD
vendors reference serials.

## Verify
Sampled wiped drives show no readable data (quick check with a recovery tool), every
disposed MFP has an erase record or certificate, and service credentials stored on them
were rotated.
