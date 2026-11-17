---
id: computing-software.digital-forensics-incident-response.evidence-handling.checking-phones-for-spyware-with-mvt
name: checking-phones-for-spyware-with-mvt
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [mvt, mobile-forensics, ios-forensics, android-forensics, spyware, dfir]
level: advanced
status: draft
description: "Use Amnesty's Mobile Verification Toolkit to check iOS backups/FFS and Android devices for spyware indicators (Pegasus, Predator): IOCs, modules and interpreting hits."
sources: ["https://docs.mvt.re/", "https://github.com/mvt-project/mvt", "https://github.com/AmnestyTech/investigations"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Checking phones for spyware with MVT

**Goal:** triage a phone belonging to an at-risk person (journalist, executive, activist) for
known mercenary spyware indicators.

## iOS
```bash
pip install mvt
mvt-ios download-iocs                                  # pulls public STIX2 indicator files
idevicebackup2 backup --full ./backup                   # after enabling encryption: idevicebackup2 encryption on <pwd>
mvt-ios decrypt-backup -p <pwd> -d ./decrypted ./backup
mvt-ios check-backup -o ./out ./decrypted               # uses downloaded IOCs automatically
mvt-ios check-fs -o ./out ./ffs_dump                    # full file system gives far more coverage
mvt-ios check-iocs --iocs pegasus.stix2 ./out           # re-check JSON results against new IOCs later
```
Modules parse Safari history, SMS/iMessage links, DataUsage/NetUsage (process names), shutdown.log,
Manifest, configuration profiles, crash reports, calendar/contacts anomalies, and more.

## Android
```bash
mvt-android check-adb -o ./out              # live over ADB: packages, processes, settings, logcat, dumpsys
mvt-android check-bugreport -o ./out bugreport.zip
mvt-android check-backup -o ./out backup.ab
```
Also review installed packages for sideloaded apps and accessibility service abuse.

## Interpreting results
- `*_detected.json` lists IOC matches (domains, process names, file paths). A match is a strong
  lead requiring expert confirmation (Amnesty Security Lab, Citizen Lab, Access Now helpline).
- No detection does not prove absence: IOCs are only for known campaigns; spyware cleans traces.
- Keep the backup/FFS as evidence; future IOC releases can be re-checked offline.

## Gotchas
- Encrypted backups contain more data than unencrypted ones; always enable encryption with a known password.
- Do not reboot or update the phone before collection; shutdown.log and process traces are fragile.
- Handle the subject's privacy carefully: the backup contains all their messages.

## Verify
Record MVT version, IOC files and their date; re-run against current IOCs before closing the case.
