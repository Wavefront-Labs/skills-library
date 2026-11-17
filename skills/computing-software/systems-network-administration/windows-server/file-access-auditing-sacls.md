---
id: computing-software.systems-network-administration.windows-server.file-access-auditing-sacls
name: file-access-auditing-sacls
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-auditing, file-access-auditing, event-4663, sacl]
level: practitioner
status: docs-checked
description: "Audit file and folder access with SACLs and the Audit File System subcategory: events 4656, 4660, 4663 and 4670, and keeping log volume sane."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-file-system
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4663
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File access auditing with SACLs

Two switches: the **audit policy** (Audit File System, success/failure) and a **SACL** on the objects. Neither
alone produces events.

## 1. Audit policy (GPO)
Enable the **Audit File System** subcategory of Advanced Audit Policy: Success, and Failure if needed.

## 2. SACL
Add auditing entries (SACL) on the folder for only the rights you care about, such as delete, write and change permissions.
Auditing everything including reads floods the log. Event 4663 generates only if the object's SACL has the required ACE.

## Events (Security log)
| ID | Meaning |
|---|---|
| 4656 | a handle to an object was requested |
| 4663 | an attempt was made to access an object |
| 4660 | an object was deleted |
| 4670 | permissions on an object were changed |

## Volume control
- Forward the Security log to a SIEM; file auditing on busy shares produces a very large number of events.
- Audit writes/deletes, not reads, unless required.

## Verify
- [ ] Deleting a test file under the audited folder yields 4663 and 4660 with the right user.

## Checked

2026-10-28. Confirmed against: Audit File System page and event 4663 page (subcategory name, events 4656, 4660, 4663, 4670 and their meanings, 4663 requires an ACE in the object's SACL). Removed (not confirmable from the cited pages): Force audit policy subcategory setting, GPO and Properties menu paths, SACL PowerShell example, Global Object Access Auditing, Get-WinEvent property indexes, log size figures.

Method: documentation only; no commands were run.
