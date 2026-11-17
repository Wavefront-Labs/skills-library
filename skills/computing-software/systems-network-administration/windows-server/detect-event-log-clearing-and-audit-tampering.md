---
id: computing-software.systems-network-administration.windows-server.detect-event-log-clearing-and-audit-tampering
name: detect-event-log-clearing-and-audit-tampering
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-auditing, event-1102, audit-policy-change, log-tampering]
level: practitioner
status: docs-checked
description: "Detect Security log clearing (event 1102) and audit policy changes (event 4719), forward logs centrally and alert on them."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4719
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detect log clearing and audit tampering

Attackers clear logs or turn auditing off to hide. The clearing itself is logged, which is why central
forwarding matters: the local copy is gone.

## Events
| Log | ID | Meaning |
|---|---|---|
| Security | **1102** | the audit log was cleared (subcategory Other Events) |
| Security | 4719 | system audit policy was changed (subcategory Audit Policy Change) |
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=1102,4719} -MaxEvents 20
```

## Prevent and detect
- Forward the Security log to a central collector or SIEM and alert on 1102 and 4719 from any server: the local copy is gone
  after a clear.

## Investigate a 1102
1. Who: the Subject fields in the event.
2. What happened just before: the SIEM still has events up to the clear.
3. Treat as an incident unless a documented change explains it.

## Verify
- [ ] Clearing the Security log on a test server raises a SIEM alert within minutes.

## Checked

2026-10-28. Confirmed against: event 1102 and event 4719 pages (event meanings and audit subcategories). Removed (not confirmable from the cited pages): event 104, 4906, 4715, 1100, 7036/7040 and Sysmon rows, user-right and log-size advice, auditpol baseline.

Method: documentation only; no commands were run.
