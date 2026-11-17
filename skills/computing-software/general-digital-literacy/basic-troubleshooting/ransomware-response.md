---
id: computing-software.general-digital-literacy.basic-troubleshooting.ransomware-response
name: ransomware-response
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, malware, ransomware, encrypted-files, ransom-note, isolate-device, restore-from-backup, no-more-ransom, report-cybercrime]
level: intro
status: draft
description: "Respond to ransomware on a home or small-office computer: disconnect, don't pay hastily, report, check No More Ransom for decryptors, wipe and restore from backup."
sources:
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
  - https://www.cisa.gov/secure-our-world
  - https://www.nomoreransom.org/
  - https://www.ncsc.gov.uk/ransomware/home
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ransomware response

**Goal:** limit damage and get your files back safely if files are encrypted and a ransom demanded.

## Signs
Files renamed with odd extensions (`.locked`, `.crypt`, random letters), won't open, a note on the
desktop or in each folder demanding payment in cryptocurrency.

## Immediately
1. **Disconnect** the device from the network: Wi-Fi off, cable out. Don't shut down yet if IT/a
   specialist may want to examine it (memory can hold keys); otherwise power off.
2. **Disconnect backup drives** and check other devices / shared drives for encrypted files.
3. Work at an organisation? Call IT/security now. Home: take photos of the ransom note.
4. From a clean device, change passwords for email, banking and cloud accounts.

## Then
- **Report** it: UK Action Fraud / Report Fraud (police), US FBI IC3 (ic3.gov), or your national CERT.
- Identify the strain and look for a free decryptor at **nomoreransom.org** (Crypto Sheriff).
- **Recover:** wipe and reinstall the OS (or reset), then restore files from a backup taken
  *before* the infection. Cloud services (OneDrive, Google Drive, Dropbox) can restore whole folders
  to an earlier date (OneDrive: *Restore your OneDrive*).
- Paying is discouraged by police: no guarantee of a key, funds crime, may be illegal in some cases
  (sanctions).

## Prevent
Offline/versioned backups (3-2-1), updates, no macro documents from email, MFA everywhere.

## Verify
- [ ] Restored files open; the rebuilt device is fully updated and scanned before reconnecting backups.
