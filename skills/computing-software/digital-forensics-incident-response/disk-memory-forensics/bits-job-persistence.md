---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.bits-job-persistence
name: bits-job-persistence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [bits-jobs, persistence, windows-event-logs, lolbins, dfir]
level: advanced
status: docs-checked
description: "Investigate BITS job abuse for download and persistence: how jobs are used (T1197), qmgr queue parsing with bits_parser, notify command lines and hardening."
sources: ["https://attack.mitre.org/techniques/T1197/", "https://learn.microsoft.com/en-us/windows/win32/bits/background-intelligent-transfer-service-portal", "https://github.com/ANSSI-FR/bits_parser"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BITS job persistence

**Goal:** Background Intelligent Transfer Service (BITS) is a legitimate transfer service for HTTP, REST and SMB downloads and uploads that resumes after network loss and reboots. ATT&CK T1197 describes abusing its jobs to download payloads, run a program when a job completes or errors, and persist through long-lived jobs.

## How abuse looks
- BITS jobs are created and managed through PowerShell and the BITSAdmin tool (both are named on the ATT&CK page).
- ATT&CK states job state lives in the BITS job database with no new files or registry modifications, and that host firewalls often permit BITS traffic.
- Persistence: long-standing jobs (the default maximum lifetime is 90 days and extendable) or an arbitrary program invoked when a job completes or errors, including after reboot. The `/SetNotifyCmdLine` option of BITSAdmin is the documented example (UBoatRAT).
- BITS uploads can also be used for exfiltration.

## Evidence
- ATT&CK's detection strategy correlates process creation, command and script telemetry, the BITS-Client operational events, and network connections initiated by BITS. Its analytic expects the notify command to be launched from `svchost.exe -k netsvcs -s BITS`.
- Job queue files: QMGR queues are usually `.dat` files (for example `qmgr0.dat`, `qmgr1.dat`) in `%ALLUSERSPROFILE%\Microsoft\Network\Downloader`. `bits_parser` (ANSSI, MIT licence) extracts jobs from a queue to CSV:
  - `bits_parser qmgr0.dat`
  - `bits_parser -o jobs.csv qmgr0.dat` writes to a file
  - `bits_parser -i image.bin` scans a full disk image for markers; slower, and the README warns results are dirtier because data from adjacent clusters can leak in. `--radiance` sets the surrounding data collected (default 2048 kB).
- Event IDs, the Windows 10 queue format and live listing commands are not covered by the cited pages; look them up in Microsoft's BITS documentation and test on a lab host before relying on them.

## Hunting
- Child processes started by the BITS service host.
- Jobs whose URLs point outside expected vendor and update domains.
- Long-lived jobs with a notify command line.

## Hardening (ATT&CK mitigations)
- Allow only legitimate BITS traffic with network and host firewall rules.
- Consider reducing the default job lifetime via Group Policy or the `JobInactivityTimeout` and `MaxDownloadTime` values under `HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\BITS`.
- Consider limiting access to the BITS interface to specific users or groups.

## Gotchas
- Windows uses BITS to download updates, and other applications use it, so baseline known update domains first.

## Verify
Each suspicious job is tied to its creating process or user, URL, payload path and any notify command executed.

## Checked
2026-11-08. Confirmed against the ATT&CK T1197 page, the Microsoft BITS portal page and the bits_parser README: BITS purpose, PowerShell and BITSAdmin interfaces, 90-day default lifetime, notify command abuse, svchost notify parent, mitigations and registry values, qmgr `.dat` location, bits_parser usage and radiance default. Removed as unconfirmed: specific Bits-Client event IDs, the qmgr.db ESE format claim, SYSTEM-owned job heuristics and live listing commands.
Method: documentation only; no commands were run.
