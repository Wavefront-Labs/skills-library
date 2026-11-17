---
id: computing-software.systems-network-administration.windows-server.enable-analytic-and-debug-event-logs
name: enable-analytic-and-debug-event-logs
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, event-logs, analytic-debug-logs, wevtutil, event-tracing, diagnostics]
level: advanced
status: docs-checked
description: "Enable hidden analytic and debug event channels with Event Viewer or wevtutil, read them, and turn them off again so they do not fill disks or lose events."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wevtutil
  - https://learn.microsoft.com/en-us/windows/win32/wes/defining-channels
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Analytic and debug event logs

Channels can be of type Admin, Operational, Analytic or Debug. Analytic and Debug channels can hold detail you need (for example SMB client and DNS server).

## Show and enable in Event Viewer
Use Event Viewer to enable the channel (for example Microsoft > Windows > SMBClient > Analytic).

## wevtutil
```cmd
wevtutil el | findstr /i smb                                  REM list channel names
wevtutil gl "Microsoft-Windows-SMBClient/Analytic"            REM config (enabled, type, maxSize)
wevtutil sl "Microsoft-Windows-SMBClient/Analytic" /e:true /ms:104857600
REM reproduce the problem
wevtutil sl "Microsoft-Windows-SMBClient/Analytic" /e:false
wevtutil qe "Microsoft-Windows-SMBClient/Analytic" /f:text /c:200 > <LOGS>\smb-analytic.txt
```
`/e` enables or disables a log and `/ms` sets the maximum size in bytes (minimum 1048576). Note `/q` on `qe` is an XPath query, not a quiet switch.

PowerShell:
```powershell
$log = Get-WinEvent -ListLog 'Microsoft-Windows-DNSServer/Analytical'
$log.IsEnabled = $true; $log.SaveChanges()
Get-WinEvent -LogName 'Microsoft-Windows-DNSServer/Analytical' -Oldest -MaxEvents 100
```
Use `-Oldest` when reading analytic/debug logs.

## Gotchas
- Size the log for the test window and disable the channel afterwards.

## Verify
- [ ] Channel captured events during the repro and is disabled again (`wevtutil gl` shows enabled: false).

## Checked
2026-10-28: Confirmed on Learn pages wevtutil and defining-channels: channel types Admin/Operational/Analytic/Debug, `wevtutil el`, `gl`, `sl` with /e and /ms (minimum 1048576 bytes), `qe` with /f and /c, /q on qe is an XPath query. Corrected: the skill used `/q:true` on `sl` as a quiet switch, but `/q` exists only on `qe`/`epl` as a query. Removed: hidden-by-default and sequential-log claims, Event Viewer menu item, -Oldest required claim, CPU cost and overwrite claims.
Method: documentation only; no commands were run.
