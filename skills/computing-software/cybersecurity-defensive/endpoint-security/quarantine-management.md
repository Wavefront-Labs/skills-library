---
id: computing-software.cybersecurity-defensive.endpoint-security.quarantine-management
name: quarantine-management
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [quarantine-management, av-quarantine, file-restore, false-positive-handling, sample-submission, antimalware]
level: practitioner
status: draft
description: "Manage anti-malware quarantine: retention, who may restore files, safe restore of false positives with allow indicators, sample submission, and collecting quarantined files."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/restore-quarantined-files-microsoft-defender-antivirus", "https://learn.microsoft.com/en-us/defender-endpoint/respond-file-alerts", "https://www.microsoft.com/en-us/wdsi/filesubmission"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quarantine management

## Policy
- Retention: Defender `QuarantinePurgeItemsAfterDelay` (default 90 days) - long enough for investigation and false-positive recovery.
- **Restore rights:** users must not restore quarantined items themselves on managed devices (Windows Security UI hidden or tamper protection; Defender policy "Allow users to see/restore" off). Restores go through the SOC.
- Notifications: users informed something was quarantined, with ticket instructions.

## Restore a false positive (Defender)
1. Confirm benign: hash reputation, signer, sandbox, vendor.
2. Submit to Microsoft as false positive (Defender portal submission / WDSI), get verdict.
3. Create an allow indicator (file hash, or certificate) scoped to device groups - prevents re-quarantine.
4. Restore: `"%ProgramFiles%\Windows Defender\MpCmdRun.exe" -Restore -Name "<ThreatName>"` or `-ListAll` to see items; Defender for Endpoint portal: file page -> "Restore from quarantine" across devices.

## Collect samples for analysis
Defender for Endpoint "Collect file" / live response `getfile`; quarantine files are encrypted and should
not be copied manually from `%ProgramData%\Microsoft\Windows Defender\Quarantine`.

## Reporting
Quarantine events into SIEM; a file quarantined on many devices at once = outbreak or false positive at scale - either way an incident.

## Gotchas
- Restoring before adding an indicator just loops (re-detected).
- Quarantined does not mean the incident is over: the dropper/initial access may still be present.
- Server-side quarantine of application files can cause outages - SOC must coordinate with owners.

## Verify
- [ ] Users cannot restore on managed devices.
- [ ] False-positive runbook tested with a benign test file.
