---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.applocker-and-wdac-logs-as-execution-evidence
name: applocker-and-wdac-logs-as-execution-evidence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [applocker-logs, evidence-of-execution, windows-event-logs, wdac, dfir]
level: practitioner
status: docs-checked
description: "Use AppLocker and WDAC (App Control) event logs to prove allowed and blocked execution, including audit-mode logging, file paths, rule names and signature details."
sources: ["https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/using-event-viewer-with-applocker", "https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/operations/event-id-explanations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AppLocker and WDAC logs as execution evidence

**Goal:** where application control is deployed, even only in audit mode, it records files it evaluated
with the path and the rule that applied. Treat those events as an execution log, with the limits below.

## AppLocker
Logs: in Event Viewer, `Application and Services Logs\Microsoft\Windows\AppLocker`, which holds the
`EXE and DLL` and `MSI and Script` logs.
| Event | Meaning |
|---|---|
| 8002 | An AppLocker rule allowed the .exe or .dll file |
| 8003 | Allowed but would have been prevented if enforced (Audit only mode) |
| 8004 | EXE or DLL prevented from running (Enforce rules mode) |
| 8005 | Script or .msi file allowed |
| 8006 | Script or .msi would have been prevented if enforced (Audit only mode) |
| 8007 | Script or MSI prevented from running (Enforce rules mode) |
| 8020-8025 | Added in Windows Server 2012 and Windows 8 (allowed, audit, prevented variants; 8023 is "allowed to be installed") |
Each event records the affected file and path (or packaged app and package identifier), whether it was
allowed or blocked, the rule type (path, file hash or publisher), the rule name and the SID of the
user or group named in the rule. Event 8001 means the policy was applied; 8000 means it was not.

## WDAC / App Control for Business
Block events are in `Applications and Services logs - Microsoft - Windows - CodeIntegrity - Operational`;
script, MSI and COM events are in `AppLocker - MSI and Script`.
| Event (CodeIntegrity) | Meaning |
|---|---|
| 3076 | Main block event for an audit-mode policy: the file would have been blocked if enforced |
| 3077 | Main block event for an enforced policy: the file was blocked |
| 3089 | Signature information for a file that was blocked or audit blocked; one event per signature, unsigned files give one event with TotalSignatureCount 0 |
| 3033 / 3034 | File did not meet policy requirements (often a revoked signature); 3034 is the audit-mode equivalent of 3033 |
| 3004 | Uncommon; typically a kernel driver tried to load with an invalid signature |
Match 3089 to its 3076/3077 event using the Correlation ActivityID in the System part of the event.

In `AppLocker - MSI and Script`: 8028 means a script host (for example PowerShell) queried App Control and
the file would have been blocked if enforced; 8029 is the enforced equivalent. The script host controls the
real behaviour (PowerShell runs disallowed script in Constrained Language Mode). 8037 means the file passed
the policy; 8038 is signing information correlated with 8028/8029; 8036 is a blocked COM object.

## Using them
- Filter the logs in Event Viewer by the IDs above; in audit mode, 8003/8006 and 3076 list what would have
  been blocked, a ready-made dataset of unusual binaries and scripts.
- Treat a block or audit event as evidence the file was evaluated or launched, and read the path and rule fields.

## Gotchas
- App Control does not generate events when a binary is allowed (3090 allow events for managed-installer or
  ISG-authorised files exist only after the TestFlags registry setting is applied and the machine restarted).
  A missing 3076/3077 is therefore not evidence of no execution.
- AppLocker logs are very verbose, particularly `EXE and DLL`; Microsoft notes you may limit forwarding of that log.
- `AppLocker - MSI and Script` events are not included on Windows Server Core.

## Checked
Date: 2026-11-07.
Read in full: Microsoft Learn "Using Event Viewer with AppLocker" (event table 8000-8040) and "Understanding App Control events" (core logs, block events, policy activation, ISG/MI diagnostics, appendix).
Confirmed: log locations, 8002-8007 meanings, 8020-8025 "added in Windows Server 2012/Windows 8", 8028/8029/8036/8037/8038, 3004/3033/3034/3076/3077/3089, correlation by ActivityID, no events for allowed binaries, 3090 TestFlags note, Server Core note.
Trimmed: the "Fqbn"/SHA-256/PID field list, "packaged app" log names and the 8020-8025 "packaged apps" label, "3033/3034 often drivers", the 1 MB default log size, the claim that 8002 is not logged by default, the Get-WinEvent snippet, VirusTotal hash matching, and the prefetch/Amcache Verify step (none on the pages).
Method: documentation only; no commands were run.
