---
id: computing-software.systems-network-administration.powershell.jea-transcripts-and-auditing
name: jea-transcripts-and-auditing
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, jea, just-enough-administration, jea-transcripts, jea-auditing, transcriptdirectory, event-4104, winrm-operational-log, audit]
level: practitioner
status: docs-checked
description: "Audit JEA use: per-session transcripts, event 4104 script block logging with ConnectedUser and RunAsUser, application logs, and WinRM event 193 for mapping run-as users."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/audit-and-report
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JEA transcripts and auditing

## Transcripts
- Configure `TranscriptDirectory` in the session configuration file (recommended). Local System writes the files, so it needs read/write access; standard users should have none, and limit which security admins can read them.
- Find transcript directories (as administrator):
```powershell
Get-PSSessionConfiguration | Where-Object { $_.TranscriptDirectory -ne $null } | Format-Table Name, TranscriptDirectory
```
- Each transcript starts with the start time, the connecting user, the RunAs user and the machine.
- Exact command syntax is not available in JEA sessions because of how commands are transformed for remoting, but the effective command is: a `CommandInvocation` line per command, `ParameterBinding` lines for each parameter and value, and a further `CommandInvocation` (usually `Out-Default`) for the output, whose InputObject is the returned object.

## PowerShell event logs
With module or script block logging enabled, the `Microsoft-Windows-PowerShell/Operational` log has event ID 4104 for each command. In JEA sessions the event includes ConnectedUser (who created the session) and RunAsUser (the account JEA used). Application event logs show changes made by the RunAsUser, so this logging is required to trace a command back to the ConnectedUser.

## Application and WinRM logs
- Other applications log only the virtual run-as user, not the connecting user. Use a session transcript, or correlate PowerShell events with time and user in the application log.
- Event ID 193 in `Microsoft-Windows-Windows Remote Management/Operational` records SID and account name of both the connecting user and the run-as user for every new JEA session.

## Related checks (same page)
- `Get-PSSessionConfiguration | Where-Object { $_.SessionType -eq 'RestrictedRemoteServer' }` finds JEA-like endpoints; the Permission property shows who may connect, and the RoleDefinitions property shows role mappings.
- `Get-PSSessionCapability -ConfigurationName <endpoint> -Username <domain\user>` shows a user's commands. It may not reflect temporary group membership from just-in-time access systems.

## Checked
Method: 2026-11-08 docs-only read of the JEA audit-and-report page (MicrosoftDocs/PowerShell-Docs markdown). Rewritten to the page; dropped unsupported detail from the old draft. Unchanged: the logging sources named above.
