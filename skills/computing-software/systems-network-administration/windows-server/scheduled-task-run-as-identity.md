---
id: computing-software.systems-network-administration.windows-server.scheduled-task-run-as-identity
name: scheduled-task-run-as-identity
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, scheduled-tasks, task-scheduler, scheduled-task-principal, logontype, s4u, gmsa, stored-credentials, network-access, least-privilege]
level: practitioner
status: docs-checked
description: "Pick the right identity for a scheduled task: SYSTEM, NETWORK SERVICE, a gMSA, S4U (no stored password, no network) or a stored-password account, and their trade-offs."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtaskprincipal
  - https://learn.microsoft.com/en-us/windows/win32/taskschd/security-contexts-for-running-tasks
  - https://learn.microsoft.com/en-us/windows/win32/taskschd/principal-logontype
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4698
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled task run-as identity

| Identity | `New-ScheduledTaskPrincipal` | Notes |
|---|---|---|
| SYSTEM / LOCAL SERVICE / NETWORK SERVICE | `-UserId SYSTEM -LogonType ServiceAccount` (or the account name) | ServiceAccount means Local System, Local Service or Network Service is the security context; no password is supplied |
| gMSA | `-UserId 'AD\gmsaTask$'` | documented as usable by scheduled tasks; the account needs batch logon rights; see the gMSA docs for the logon type |
| User, S4U | `-UserId 'AD\svc-x' -LogonType S4U` | no password stored; **no access to the network or encrypted files** |
| User, Password | `Register-ScheduledTask ... -User AD\svc-x -Password <...>` | password must be supplied at registration |
| Interactive only | `-LogonType Interactive` | user must already be logged on; runs only in an existing interactive session |

## Choosing
- Local-only maintenance: a service account (SYSTEM, or LOCAL SERVICE / NETWORK SERVICE for least privilege).
- Needs network resources: a gMSA with only the rights it needs, instead of a stored password.
- Avoid stored-password user accounts: for `<LogonType>Password</LogonType>` tasks Microsoft's event 4698 guidance
  says the password is saved in Credential Manager in cleartext and can be extracted with administrative privileges.
- S4U suits local-only jobs under a specific user without storing a password; it cannot reach the network.
- `-RunLevel Highest` runs with the highest privileges; `Limited` uses the least-privileged account. With UAC on, tasks
  run with low privileges by default.
- A group cannot be the security context with the S4U or Password logon types.
## Updating a stored password across servers (if you must)
```powershell
Set-ScheduledTask -TaskName 'Legacy job' -User 'AD\svc-legacy' -Password '<NEW_PASSWORD>' -CimSession $servers
```
Better: migrate it to a gMSA.

## Verify
- [ ] `Get-ScheduledTask | Select TaskName,@{n='RunAs';e={$_.Principal.UserId}},@{n='Logon';e={$_.Principal.LogonType}}` shows no unexpected Password-type tasks.
- [ ] Tasks needing network access succeed (LastTaskResult 0) under their gMSA.

## Checked

2026-10-26 against the Task Scheduler docs (win32 Principal.LogonType, security contexts for running tasks, error constants; last commit 2026-10-08), the ScheduledTasks module reference for Windows Server 2025 (New-ScheduledTaskPrincipal logon types and run levels, Set-ScheduledTask -User/-Password/-CimSession) and the Windows 10 event 4698 reference (archived Microsoft docs): logon type meanings, S4U having no network access, RunLevel values, group restriction, batch-logon requirement, and the cleartext-password warning. Removed unconfirmed per-account network identity claims, the LSA-secret wording and the gMSA LogonType Password example.

Method: documentation only; no commands were run.
