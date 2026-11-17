---
id: computing-software.it-support-helpdesk.remote-support-tools.pulling-event-logs-remotely
name: pulling-event-logs-remotely
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, remote-log-collection, event-logs, get-winevent, wevtutil]
level: practitioner
status: docs-checked
description: "Collect logs from a remote Windows endpoint without a screen session: Get-WinEvent filters, wevtutil exports to .evtx, and Intune collect diagnostics."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wevtutil"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/collect-diagnostics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pulling-event-logs-remotely

## Windows: query in place
Filter at the source; do not pull a whole log over the wire and filter locally.
`Get-WinEvent -FilterHashtable` takes keys such as `LogName`, `Level` and `StartTime`
(also `ProviderName`); run it on the remote machine with `Invoke-Command`:
```powershell
Invoke-Command -ComputerName PC01 -ScriptBlock {
  Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2; StartTime=(Get-Date).AddDays(-2)} |
    Select-Object TimeCreated, Id, ProviderName, Message
}
```
`Get-WinEvent` also has its own `-ComputerName` parameter for local and remote computers
(the cmdlet page has examples for one and several servers).

## Windows: export for offline analysis
`wevtutil epl <Logname> <file>.evtx` exports a log (optionally with `/q:<Query>` to filter);
`wevtutil el` lists log names; `wevtutil al <file>` archives an exported log. The remote
switch `/r:<Remote>` is documented on the wevtutil page. Open the .evtx in Event Viewer.

## Without network reach
- Intune **Collect diagnostics** (remote action on a device) produces a data zip you
  download from the portal; the page lists what it contains (MDM logs cab, msinfo32 report,
  battery and energy reports and more). Check the page for supported platforms and versions.
- An RMM script can zip logs and upload them to the RMM file store.

## Gotchas
- Logs may contain user data; handle exports under your data-handling rules.

## Verify
You have the events covering the fault window, saved to the ticket or case store, and the
collection method is noted.

## Checked
2026-11-01. Confirmed on Microsoft Learn Get-WinEvent (FilterHashtable LogName/Level/
StartTime/ProviderName, remote computer examples), wevtutil (el, epl, al, /q, /r) and Intune
Collect diagnostics (zip download, contents). Removed: firewall/RPC requirement, event IDs
41/6008/1000/1001, Event Log Readers requirement, provider DLL note, macOS and Linux log
commands (not covered by these sources).
Method: documentation only; no commands were run.
