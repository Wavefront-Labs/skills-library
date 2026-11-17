---
id: computing-software.systems-network-administration.windows-server.nps-logging-and-reason-codes
name: nps-logging-and-reason-codes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, nps, network-policy-server, nps-logging, event-6273, event-6272, reason-codes, accounting-logs, audit-network-policy-server, iaslog, troubleshooting]
level: practitioner
status: gated
description: "Troubleshoot NPS with event 6272/6273 reason codes, enable the Network Policy Server audit subcategory, and configure accounting logs (text or SQL)."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-accounting-configure
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc735399(v=ws.10)
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NPS logging and reason codes

## Enable auditing
```cmd
auditpol /set /subcategory:"Network Policy Server" /success:enable /failure:enable
```
This subcategory name and the equivalent Advanced Audit Policy path (Logon/Logoff > Audit Network Policy Server) are (gated: unconfirmed, source is paywalled or blocked).
NPS also supports event logging configured in the NPS console properties.

## Read event 6273 (access denied)
Event 6273, source Microsoft-Windows-Security-Auditing, has the message "Network Policy Server denied access to a user".
Its fields include User, Client Machine, Called and Calling Station Identifier, NAS, RADIUS Client, **Proxy Policy Name**
(the connection request policy), **Network Policy Name**, Authentication Provider and Type, EAP Type, **Reason Code** and **Reason**.
Documented causes: invalid credentials, a connection method the network policy does not allow, a NAS under attack,
NPS unable to reach the user account database on the domain controller, or NPS log files or the SQL Server database unavailable.

| Reason code | Meaning |
|---|---|
| 16 | authentication failed (gated: unconfirmed, source is paywalled or blocked) |
| 23 | error during EAP processing (gated: unconfirmed, source is paywalled or blocked) |
| 48 | no network policy matched (gated: unconfirmed, source is paywalled or blocked) |
| 49 | no connection request policy matched (gated: unconfirmed, source is paywalled or blocked) |
| 65 | dial-in permission denied on the account (gated: unconfirmed, source is paywalled or blocked) |
| 66 | authentication method not enabled in the policy (gated: unconfirmed, source is paywalled or blocked) |
| 8 | account does not exist (gated: unconfirmed, source is paywalled or blocked) |

The reason-code table was not found in the public documentation that could be read; use the Reason text in the event itself.

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=6273; StartTime=(Get-Date).AddHours(-1)} |
  Select TimeCreated, Message
```

## Accounting
NPS console > Accounting: text log files or SQL Server logging. Log file defaults: directory under `%SystemRoot%\System32\LogFiles`,
format DTS Compliant (legacy ODBC and IAS formats are also available), new file at 10 MB by default.
- Keep logs on a separate partition from the system partition. If accounting fails because the disk is full, NPS stops processing requests when "If logging fails, discard connection requests" is set; the setting is in the Logging failure action.
- SQL Server logging sends XML to the `report_event` stored procedure of the designated database; a text-file failover can be enabled.

## Verify
- [ ] A failed test authentication produces event 6273 with a Reason.
- [ ] Accounting files rotate and disk space is monitored.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23), the windows-powershell-docs NPS cmdlet pages and the MicrosoftDocs/entra-docs repository. Confirmed event 6273 identity, message and field names (Proxy Policy Name, Network Policy Name, Reason Code, Reason), the documented causes, log directory, DTS format and 10 MB default size, the discard-on-failure setting and report_event stored procedure. Corrected: the connection request policy appears as Proxy Policy Name. The auditpol subcategory string and the reason code table could not be confirmed from readable public documentation and are marked gated; removed the IN*.log name and iasparse advice.

Method: documentation only; no commands were run.
