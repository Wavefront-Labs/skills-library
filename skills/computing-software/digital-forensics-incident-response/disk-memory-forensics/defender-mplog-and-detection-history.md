---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.defender-mplog-and-detection-history
name: defender-mplog-and-detection-history
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [defender-mplog, evidence-of-execution, windows-defender, anti-forensics, dfir]
level: advanced
status: draft
description: "Mine Microsoft Defender logs for evidence: MPLog process and file activity, Detection History files, quarantine, event 1116/1117/5001/5007, and tampering traces."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/troubleshoot-microsoft-defender-antivirus", "https://www.crowdstrike.com/blog/how-to-use-microsoft-protection-logging-for-forensic-investigations/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defender MPLog and detection history

**Goal:** even without EDR, built-in Microsoft Defender Antivirus keeps detailed logs that record
executables, scan results and configuration changes.

## Sources
| Source | Location | Content |
|---|---|---|
| MPLog | `%ProgramData%\Microsoft\Windows Defender\Support\MPLog-*.log` | Text log: `SDN` (submitted file hash queries), `EstimatedImpact` lines with process image paths and PIDs, scan results, engine/signature updates, exclusions |
| MPDetection logs | same folder `MPDetection-*.log` | Detection events |
| Detection History | `%ProgramData%\Microsoft\Windows Defender\Scans\History\Service\DetectionHistory\` | Binary files per detection: threat name, file path, user, process that wrote it |
| Quarantine | `%ProgramData%\Microsoft\Windows Defender\Quarantine\` | Encrypted copies (RC4 with a known key; tools like `defender-dump` restore them) |
| Event log | `Microsoft-Windows-Windows Defender/Operational` | 1116 detected, 1117 action taken, 1118/1119 failures, 5001 real-time protection disabled, 5007 configuration changed, 5013 tamper protection blocked change |

## Investigative uses
- **Execution:** MPLog `EstimatedImpact` / performance lines name processes that caused file
  activity (e.g. `ProcessImageName: rclone.exe`), with times - evidence of tools long since deleted.
- **Hashes:** SDN entries give SHA-1/SHA-256 of files Defender checked.
- **Tampering:** 5007 showing new exclusion paths (`Exclusions\Paths\<path>` in the event) or
  `DisableRealtimeMonitoring`; 5001 real-time disabled - classic ransomware precursors.
- **Recover samples** from quarantine for analysis.

## Gotchas
- MPLog rotates; collect early (KAPE target `WindowsDefender`).
- MPLog times are in UTC in most lines; confirm against event logs.
- Exclusions also live in the registry `HKLM\SOFTWARE\Microsoft\Windows Defender\Exclusions` - check key last-write time.

## Verify
Defender events and MPLog lines for the same file/time agree, and recovered quarantine files hash-match the logged values.
