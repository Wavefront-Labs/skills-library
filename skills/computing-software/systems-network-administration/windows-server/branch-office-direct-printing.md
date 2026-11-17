---
id: computing-software.systems-network-administration.windows-server.branch-office-direct-printing
name: branch-office-direct-printing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, print-services, branch-office-direct-printing, print-management, wan-optimization]
level: practitioner
status: docs-checked
description: "Enable Branch Office Direct Printing so branch clients print straight to local printers while the print server keeps drivers, queues and management."
sources:
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/jj134152(v=ws.11)
  - https://learn.microsoft.com/en-us/powershell/module/printmanagement/set-printer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Branch Office Direct Printing

Normally a branch print job goes client > central print server (over WAN) > branch printer (over WAN again).
Branch Office Direct Printing (BODP) sends the job straight from the client to the printer; the server still
provides the driver, queue settings and status.

## Enable per printer
Enable it per printer; the setting is the `-RenderingMode` BranchOffice value in PowerShell.
```powershell
Set-Printer -ComputerName PRINT01 -Name 'BR1-MFP-01' -RenderingMode BranchOffice
Get-Printer -ComputerName PRINT01 | ft Name,RenderingMode
```

## Requirements and limits
- Not usable when the queue is configured for server side rendering (SSR). To re-enable it, enable 'Render Jobs On Client' on the server queue.

## Job logging
Quota, auditing and detailed job logging capabilities are lost when Branch Office Direct Printing is used. `Set-Printer` has `-DisableBranchOfficeLogging` and `-BranchOfficeOfflineLogSizeMB` for branch office logging.

## Verify
- [ ] A network capture shows the branch client sending the job directly to the printer.

## Checked
2026-10-28: Confirmed on Learn pages Branch Office Direct Printing (Windows Server 2012 R2 doc) and set-printer: -RenderingMode (SSR, CSR, BranchOffice), SSR prevents BODP, 'Render Jobs On Client' setting, quota/auditing/detailed job logging are lost, -DisableBranchOfficeLogging and -BranchOfficeOfflineLogSizeMB. Corrected: the skill said the job still appears in server history; the page says job logging is lost. Removed: console path, version and port requirements, shadow queue claim, PrintService log and refresh tips.
Method: documentation only; no commands were run.
