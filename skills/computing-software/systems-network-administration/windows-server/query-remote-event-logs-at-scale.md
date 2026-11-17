---
id: computing-software.systems-network-administration.windows-server.query-remote-event-logs-at-scale
name: query-remote-event-logs-at-scale
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, event-logs, remote-event-log, get-winevent, invoke-command, wevtutil]
level: practitioner
status: docs-checked
description: "Query event logs on many servers quickly: Get-WinEvent -ComputerName vs Invoke-Command fan-out, filter early, handle unreachable hosts, and export results."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/invoke-command
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query remote event logs at scale

## One server
```powershell
Get-WinEvent -ComputerName SRV01 -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddDays(-1)}
```
Remote access needs the firewall port for the event log service to be open.

## Many servers: fan out
```powershell
$servers = Get-Content servers.txt
$res = Invoke-Command -ComputerName $servers -ThrottleLimit 64 -ErrorAction SilentlyContinue -ErrorVariable bad -ScriptBlock {
  Get-WinEvent -FilterHashtable @{LogName='System'; Id=41,6008,1074; StartTime=(Get-Date).AddDays(-7)} -ErrorAction SilentlyContinue |
    Select TimeCreated,Id,ProviderName,@{n='Msg';e={$_.Message -replace '\s+',' '}}
}
$res | Select PSComputerName,TimeCreated,Id,Msg | Export-Csv unexpected-reboots.csv -NoTypeInformation
$bad | % { $_.TargetObject }      # unreachable hosts
```

## Filter on the server
- Always FilterHashtable or FilterXPath, never `Get-WinEvent | Where` on a whole log.
- Add `-ErrorAction SilentlyContinue` inside the block so servers without matching events do not abort the run.

## Verify
- [ ] Results include PSComputerName for each event; the unreachable list is reviewed, not silently dropped.

## Checked
2026-10-28: Confirmed on Learn pages get-winevent and invoke-command: Get-WinEvent -ComputerName, -FilterHashtable/-FilterXPath, Invoke-Command -ThrottleLimit, firewall port for remote event log access; event IDs 41, 6008, 1074 appear in the unexpected-reboot troubleshooting page. Removed: RPC group and serial claims, performance claim, message-rendering tip, wevtutil remote example, WEF/AMA alternative.
Method: documentation only; no commands were run.
