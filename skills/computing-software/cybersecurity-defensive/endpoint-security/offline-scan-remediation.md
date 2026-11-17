---
id: computing-software.cybersecurity-defensive.endpoint-security.offline-scan-remediation
name: offline-scan-remediation
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [offline-scan, defender-offline, boot-time-scan, rootkit-remediation, bootable-rescue-media, antimalware]
level: practitioner
status: docs-checked
description: "Use offline scanning to remediate rootkits and persistent malware: Defender Offline scan, vendor rescue media, when to scan vs reimage, and preserving evidence first."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-offline", "https://learn.microsoft.com/en-us/powershell/module/defender/start-mpwdoscan", "https://csrc.nist.gov/pubs/sp/800/83/r1/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline scanning and remediation

Malware that hides from a running OS (rootkits, bootkits, files locked by malicious drivers) is easier to
detect when the OS is not running.

## Microsoft Defender Offline
- Starts a scan from the Windows Recovery Environment after reboot, using current definitions.
- Trigger: Windows Security -> Virus & threat protection -> Scan options -> Microsoft Defender Offline scan; or `Start-MpWDOScan`.
- Results: `Get-MpThreatDetection` after reboot, Protection history, event log `Microsoft-Windows-Windows Defender/Operational`.
- The device is unavailable during the scan - schedule with the user.

## Vendor rescue media
Kaspersky Rescue Disk, ESET SysRescue, Bitdefender Rescue Environment - bootable images to scan when the OS
will not boot. BitLocker-protected volumes need the recovery key to be scanned.

## Decision: clean or reimage
| Situation | Action |
|---|---|
| Commodity adware/PUA, clear detection and removal | Clean, monitor |
| Rootkit/bootkit, firmware indicators, unknown persistence | **Reimage** (and consider firmware reflash) |
| Hands-on-keyboard intrusion | Reimage after forensic collection; rotate credentials used on the host |
NIST SP 800-83: rebuilding is the most reliable way to restore integrity after significant compromise.

## Evidence first
Before offline scans or reimaging on incident devices: memory capture and triage collection (see
endpoint-isolation-and-forensic-triage); scans modify/delete artefacts.

## Gotchas
- Offline scan needs the device to boot into WinRE; broken WinRE (common after disk changes) prevents it - check `reagentc /info`.
- Secure Boot bootkits (BlackLotus) need revocation updates (DBX) and boot media changes, not just scanning.

## Checked
2026-10-28. Confirmed in the Microsoft Defender Offline and Start-MpWDOScan pages: offline scan from the recovery environment, `Start-MpWDOScan`, `Get-MpThreatDetection` cmdlet. Removed: the Intune remote action name and the ~15 minute duration.
Method: documentation only; no commands were run.

## Verify
- [ ] Post-scan full scan clean; EDR shows no reappearing persistence after 7 days.
