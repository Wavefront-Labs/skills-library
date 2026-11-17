---
id: computing-software.digital-privacy-hygiene.device-hardening.autoruns-persistence-check
name: autoruns-persistence-check
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, autoruns, malware-removal, microsoft-defender]
level: practitioner
status: draft
description: "Use Sysinternals Autoruns to find malware persistence on Windows: hide Microsoft entries, verify signatures, check VirusTotal, and disable safely."
sources:
  - "https://learn.microsoft.com/sysinternals/downloads/autoruns"
  - "https://learn.microsoft.com/sysinternals/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Autoruns persistence check

**Goal:** list everything that starts automatically on a Windows PC and spot what shouldn't be there.

## Run
Download Autoruns from Microsoft Sysinternals, run `Autoruns64.exe` **as administrator**.

## Configure
- Options > **Hide Microsoft Entries** and **Hide Windows Entries**.
- Options > Scan Options > **Verify code signatures** and **Check VirusTotal.com** (sends file hashes only, unless
  you choose to submit unknown files). Rescan (F5).

## Read
| Colour/flag | Meaning |
|---|---|
| Pink/red row | No verified publisher or file details; investigate |
| Yellow | Entry points to a missing file (leftover) |
| VirusTotal "x/70" | Detections; >2-3 engines warrants action |

Tabs to check: **Logon** (Run keys, Startup folder), **Scheduled Tasks**, **Services**, **Explorer**,
**Browser extensions**, **WMI**, **Image Hijacks**.

## Acting
- **Uncheck** to disable (reversible) rather than delete. Reboot and confirm the system works.
- Delete only once confirmed malicious; also remove the file it points to.
- Unknown signed software: search the publisher before removing.

## Baseline
File > Save on a clean system; later File > Compare to highlight new entries. CLI for scripting:
```
autorunsc64.exe -accepteula -a * -c -h -s -v > autoruns.csv
```

## Gotchas
- Malware sometimes masquerades with Microsoft-like names in user folders; check paths (`AppData\Roaming\...`).
- Disabling security software entries breaks protection; leave Defender entries alone.
