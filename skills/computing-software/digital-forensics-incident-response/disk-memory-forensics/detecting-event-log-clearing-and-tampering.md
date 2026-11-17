---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.detecting-event-log-clearing-and-tampering
name: detecting-event-log-clearing-and-tampering
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [log-clearing, anti-forensics, 1102, evtx, event-log-tampering, dfir]
level: practitioner
status: docs-checked
description: "Detect Windows event log clearing and audit policy tampering via Security events 1102 and 4719, clearing commands and forwarded copies."
sources: ["https://attack.mitre.org/techniques/T1685/005/", "https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-1102", "https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4719"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting event log clearing and tampering

**Goal:** show whether Windows logs were cleared or audit settings changed, and who did it.

## Direct evidence (from the pages)
- **Security 1102, "The audit log was cleared."** Generated every time the Windows Security audit log is cleared (Windows Server 2008 / Vista and later). Fields: SubjectUserSid, SubjectUserName, SubjectDomainName, SubjectLogonId. The Logon ID can be correlated with recent events such as 4624. Microsoft says you should not normally see this event, as there is rarely a need to clear the Security log, and recommends monitoring it and investigating why.
- **Security 4719, "System audit policy was changed."** Generated when the computer's audit policy changes, and always logged regardless of the Audit Policy Change subcategory setting. Fields include the subject, category, subcategory and its GUID, and the change: Success or Failure added or removed. `auditpol /list /subcategory:* /v` lists subcategory GUIDs. Microsoft recommends monitoring all of these, especially on high-value assets, and investigating unplanned changes.
- The ATT&CK sub-technique "Clear Windows Event Logs" (now T1685.005; the older T1070.001 URL redirects there) lists these methods: `wevtutil cl system|application|security` with administrator rights, the Event Viewer GUI, PowerShell (for example `Remove-EventLog -LogName Security`, which can delete the log and disable future logging after a reboot, with events possibly still written to the `.evtx` between the command and the reboot), and deleting the stored log files directly under the `winevt\logs` folder of the Windows system directory.

## Indirect evidence (practice; the pages do not describe these)
- Command-line or script-block evidence of the commands above, if process creation or PowerShell logging was enabled and forwarded.
- Missing `.evtx` files, or a Security log that is unusually small or starts at the time of a 1102.
- Silence periods across channels, or events present in a forwarded copy (SIEM, log collector) that are missing locally.
- Memory images and older copies of the logs (volume shadow copies, backups) may hold records that were later cleared.

## Mitigation noted by ATT&CK
Forward events to a log server or data repository automatically and with minimal delay, and protect locally stored event files with permissions.

## Verify
Report the 1102 or 4719 time, the account and logon ID, the silence window, and which records were recovered from which copy.

## Checked

2026-11-09. Read in full: Microsoft Learn event 1102 and 4719 pages (description, fields, versions, monitoring recommendations) and the MITRE ATT&CK page for Clear Windows Event Logs (description, mitigations, detection summary). Removed: System 104, Security 1100, services 7036/7034, `wevtutil sl` and the registry channel-disable paths, `auditpol /clear`, the EventRecordID-gap claim, Invoke-Phant0m, the MFT/USN checks and the EVTXtract/bulk_extractor carving commands (EVTXtract GitHub source not read). The indirect-evidence list is practice.

Method: documentation only; no commands were run.
