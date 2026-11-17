---
id: computing-software.systems-network-administration.windows-server.get-winevent-filterhashtable-and-xpath
name: get-winevent-filterhashtable-and-xpath
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, event-logs, event-viewer, get-winevent, filterhashtable, filterxpath, event-xml, remote-event-query]
level: practitioner
status: docs-checked
description: "Query Windows event logs efficiently with Get-WinEvent: FilterHashtable, XPath and FilterXml, extracting EventData fields, remote queries and offline .evtx files."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent
  - https://learn.microsoft.com/en-us/powershell/scripting/samples/creating-get-winevent-queries-with-filterhashtable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Query events with Get-WinEvent

## Fast filtering (server-side)
Never `Get-WinEvent -LogName Security | Where ...` on a big log: filter at the source.
```powershell
Get-WinEvent -FilterHashtable @{ LogName='System'; Level=1,2; StartTime=(Get-Date).AddHours(-24) }
Get-WinEvent -FilterHashtable @{ LogName='Security'; Id=4625; StartTime=(Get-Date).AddDays(-1) } -MaxEvents 200
Get-WinEvent -FilterHashtable @{ LogName='Security'; Id=4624; Data='10' }   # match any EventData value
```
Keys include LogName, ProviderName, Path, Keywords, ID, Level, StartTime, EndTime, UserID and Data (see the FilterHashtable page for the full table).

## XPath for precise matches
```powershell
$x = "*[System[(EventID=4624)]] and *[EventData[Data[@Name='LogonType']='10'] and EventData[Data[@Name='TargetUserName']='admin']]"
Get-WinEvent -LogName Security -FilterXPath $x -MaxEvents 50
```
Build XPath/XML in Event Viewer (Filter Current Log > XML tab) and paste into
`-FilterXml`.

## Extract fields
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4625} -MaxEvents 100 | ForEach-Object {
  $d = ([xml]$_.ToXml()).Event.EventData.Data
  $d | Select-Object Name,'#text' }
```

## Remote and offline
```powershell
Get-WinEvent -ComputerName DC01 -FilterHashtable @{LogName='Directory Service';Level=2}
Invoke-Command DC01,DC02 { Get-WinEvent -FilterHashtable @{LogName='System';Id=1074} -MaxEvents 5 }   # parallel
Get-WinEvent -Path '<vol>:\Cases\Security.evtx' -FilterXPath '*[System[EventID=1102]]'
Get-WinEvent -ListLog *
```
Add `-ErrorAction SilentlyContinue` in scripts when an empty result is expected.

## Verify
- [ ] Queries use FilterHashtable, FilterXPath or FilterXml instead of Where-Object on a whole log.

## Checked
2026-10-28: Confirmed on Learn pages get-winevent and creating-get-winevent-queries-with-filterhashtable: -FilterHashtable keys (including UserID and Data), -FilterXPath, -FilterXml, -ListLog, -Path, -ComputerName, -ErrorAction. Removed: Level number meanings, named EventData key version note, event 1129 example, specific field names in the extraction example, RecordCount/LastWriteTime listing, exact error text.
Method: documentation only; no commands were run.
