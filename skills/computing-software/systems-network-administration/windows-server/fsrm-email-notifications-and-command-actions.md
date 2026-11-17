---
id: computing-software.systems-network-administration.windows-server.fsrm-email-notifications-and-command-actions
name: fsrm-email-notifications-and-command-actions
category: computing-software
field: systems-network-administration
product: windows-server
tags: [fsrm, fsrm-notifications, fsrm-quotas, file-screening, event-log-actions]
level: practitioner
status: docs-checked
description: "Configure FSRM notifications: SMTP settings, email message variables, event log entries and command actions for quota and file screen events with rate limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/fsrm/configure-email-notifications.md
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/new-fsrmaction
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/set-fsrmsetting
  - https://learn.microsoft.com/en-us/powershell/module/fileserverresourcemanager/send-fsrmtestemail
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSRM email notifications and command actions

## SMTP
```powershell
Set-FsrmSetting -SmtpServer smtp.corp.example.com -AdminEmailAddress 'fileops@example.com' -FromEmailAddress 'fsrm@fs01.corp.example.com'
Send-FsrmTestEmail -ToEmailAddress 'fileops@example.com'
```
The FSRM options page asks only for the SMTP server name or IP address; check relay acceptance rules for the file server with your mail team.

## Actions on a quota threshold or file screen
```powershell
$mail = New-FsrmAction -Type Email -MailTo '[Admin Email]' `
  -Subject 'Quota threshold reached' `
  -Body 'A quota threshold was reached on the file server.' -RunLimitInterval 60
$evt  = New-FsrmAction -Type Event -EventType Warning -Body 'A quota threshold was reached on the file server.' -RunLimitInterval 60
$thr  = New-FsrmQuotaThreshold -Percentage 90 -Action $mail,$evt
Set-FsrmQuota -Path <DATA_VOLUME>\Home\jdoe -Threshold $thr
```
- `-RunLimitInterval` is the minimum number of minutes before the server can run the action again, which limits repeat mails; Set-FsrmSetting also has `-EmailNotificationLimit`, `-EventNotificationLimit`, `-CommandNotificationLimit` and `-ReportNotificationLimit`.
- Variables in brackets are expanded; `[Admin Email]` is valid in `-MailTo`, and the cmdlet examples use `[File Owner]` and `[source file path]`.

## Command actions (file screen = ransomware tripwire)
```powershell
$cmd = New-FsrmAction -Type Command -Command "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" `
  -CommandParameters '-NoProfile -File <DATA_VOLUME>\Scripts\Block-SmbUser.ps1 -User "[File Owner]"' `
  -SecurityLevel LocalSystem -KillTimeOut 5 -WorkingDirectory '<DATA_VOLUME>\Scripts' -RunLimitInterval 0
```
A typical script denies the offending user on the share (`Block-SmbShareAccess`) and alerts. `-KillTimeOut` is in minutes. Store scripts on a path
only admins can write; with `-SecurityLevel LocalSystem` FSRM runs them as SYSTEM.

## Event log
`New-FsrmAction -Type Event` writes an event with the chosen `-EventType` (None, Information, Warning, Error); forward those events to the SIEM.

## Verify
- [ ] Test email received; a test file screen hit produces mail, event and command action within seconds.

## Checked
Release checked: windowsserverdocs and windows-powershell-docs (Windows Server 2025 docset), GitHub main as of 2026-10-23.
- New-FsrmAction: -Type Email/Event/Command/Report, -RunLimitInterval (minutes), -KillTimeOut (minutes), -SecurityLevel (None, NetworkService, LocalService, LocalSystem), -EventType values; Set-FsrmSetting -SmtpServer, -AdminEmailAddress, -FromEmailAddress and the four notification-limit parameters; Send-FsrmTestEmail -ToEmailAddress.
- configure-email-notifications page: SMTP server name or IP is the only mail transport setting.
- Removed unconfirmed details: the unauthenticated port 25 relay requirement, `[Source Io Owner]`-style variables and the Insert Variable dialog, and the SRMSVC event ids.

Method: documentation only; no commands were run.
