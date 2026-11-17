---
id: computing-software.digital-privacy-hygiene.device-hardening.responding-to-ransomware-on-a-home-pc
name: responding-to-ransomware-on-a-home-pc
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, ransomware-response, malware-removal, offline-backup]
level: practitioner
status: draft
description: "Respond to ransomware on a home computer: isolate it, protect backups, identify the strain, check free decryptors, report, wipe and restore."
sources:
  - "https://www.nomoreransom.org/"
  - "https://www.cisa.gov/stopransomware/ransomware-guide"
  - "https://www.ic3.gov/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Responding to ransomware on a home PC

**Goal:** limit the spread, recover files without paying if possible, and rebuild cleanly.

## Immediately
1. **Disconnect** the PC from the network (Wi-Fi off, unplug Ethernet). Don't connect backup drives.
2. Unplug any external drives and NAS shares; check other devices on the network for encrypted files.
3. Photograph the ransom note and note the file extension of encrypted files.
4. From a different, clean device: change passwords for email and accounts used on that PC.

## Identify and look for decryptors
- Upload the ransom note/an encrypted sample to **ID Ransomware** to identify the family.
- Check **No More Ransom** (nomoreransom.org) for a free decryptor for that family.
- Keep encrypted files even if no decryptor exists today; one may appear later.

## Cloud files
- OneDrive: **Restore your OneDrive** (Microsoft 365) to a time before the encryption; or version history per file.
- Dropbox: Rewind; Google Drive: version history per file.

## Report
FBI IC3 (US) or your national cyber agency; your bank if payment details were on the PC. Law enforcement advises
not paying: payment funds attacks and doesn't guarantee recovery.

## Rebuild
Wipe and reinstall the OS (don't just "clean"), update, then restore from backups made before the infection; scan
backups first.

## Prevent repeat
Offline/versioned backups, Controlled folder access, standard user account, updates.

## Gotchas
- Some ransomware also steals data; assume documents on the PC may be published and act on sensitive items.
