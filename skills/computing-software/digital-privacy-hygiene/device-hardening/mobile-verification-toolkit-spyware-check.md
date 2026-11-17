---
id: computing-software.digital-privacy-hygiene.device-hardening.mobile-verification-toolkit-spyware-check
name: mobile-verification-toolkit-spyware-check
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, mobile-verification-toolkit, mvt, mercenary-spyware, pegasus, ios-backup-analysis, iocs, amnesty-tech, malware]
level: advanced
status: draft
description: "Check an iPhone or Android for known mercenary spyware indicators with Amnesty's Mobile Verification Toolkit (mvt-ios, mvt-android) against published IOCs."
sources:
  - "https://docs.mvt.re/"
  - "https://github.com/mvt-project/mvt"
  - "https://www.accessnow.org/help/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile Verification Toolkit spyware check

**Goal:** for journalists, activists and others who receive Apple/Google threat
notifications or suspect targeting, look for traces of known spyware (Pegasus, Predator
etc.). MVT checks for **known indicators**; a clean result isn't proof of a clean phone.

## Before you start
If you received an Apple threat notification or are high risk, contact **Access Now's
Digital Security Helpline** or Amnesty Tech; they analyse for free and handle evidence
properly. Enable Lockdown Mode meanwhile.

## iPhone (encrypted backup analysis)
```bash
pip3 install mvt
# make an encrypted local backup (Finder on macOS, or libimobiledevice):
idevicebackup2 backup --full /path/to/backup        # set backup encryption password first
mvt-ios decrypt-backup -p <BACKUP_PASSWORD> -d /path/to/decrypted /path/to/backup
mvt-ios download-iocs                                 # fetch public indicator files
mvt-ios check-backup --output /path/to/results /path/to/decrypted
```
Look at `*_detected.json` files in results; detections list matching domains/processes.

## Android
```bash
mvt-android download-iocs
mvt-android check-adb --output /path/to/results       # USB debugging enabled
# or analyse an androidqf collection: mvt-android check-androidqf ...
```
Android coverage is narrower than iOS.

## Interpreting
- Detections: preserve the backup and results, contact a helpline; don't wipe the phone yet
  (evidence).
- No detections: good sign for known campaigns only; keep phone updated and Lockdown Mode
  on if high risk; reboot daily (helps against some non-persistent exploits).

## Verify
- [ ] IOCs updated the same day as the scan.
- [ ] Results reviewed; any detection escalated to a helpline.
