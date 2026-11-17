---
id: computing-software.it-support-helpdesk.desktop-support.clearing-a-stuck-print-spooler
name: clearing-a-stuck-print-spooler
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, printer, printing, print-spooler-reset, print-queue, spoolsv, printservice-log, stuck-print-job, printer-offline]
level: intro
status: docs-checked
description: "Clear stuck print jobs and a crashing spooler on Windows clients and print servers, find the bad job or driver, and fix 'printer offline' that isn't really offline."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/printing/print-spooler-service-not-running"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/printing/new-printer-status-is-offline"
  - "https://support.microsoft.com/en-us/windows/hardware/printer/fix-printer-connection-and-printing-problems-in-windows"
  - "https://learn.microsoft.com/en-us/powershell/module/printmanagement/get-printjob"
  - "https://learn.microsoft.com/en-us/powershell/module/printmanagement/remove-printjob"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# clearing-a-stuck-print-spooler

Goal: the queue moves again in two minutes, and if it keeps sticking you
know which job or driver to blame.

## Clear a stuck queue
```powershell
Get-PrintJob -PrinterName "Finance-MFP" | Select Id, DocumentName, UserName, JobStatus, Size
Remove-PrintJob -PrinterName "Finance-MFP" -ID 12
```
Restarting the spooler also clears stuck jobs (elevated prompt):
```powershell
Restart-Service -Name spooler
```
If jobs will not delete, stop the service, delete everything in the spool
folder, and start it again (Microsoft's documented reset):
```cmd
net stop spooler
del /q %windir%\system32\spool\PRINTERS\*.*
net start spooler
```
On a print server this deletes **everyone's** queued jobs; announce first.

## Spooler will not stay running
Microsoft's checklist for "Print Spooler service not running":
- Restart the service and check the event logs for errors initialising the
  local print provider; look for system instability or low resources.
- Check that no Group Policy disables or stops the Print Spooler (disabling
  it is sometimes applied as a security mitigation, including on domain
  controllers by design).
- Update drivers; outdated drivers and print components can make the
  spooler stop responding.
- Check anti-virus: create exclusions for the spool folder.

## "Printer offline"
- Right-click the queue and clear **Use Printer Offline**. When a queue is
  deleted while Offline and a same-named queue is added, the new one can
  inherit the Offline state from the registry value `PrinterOnLine` = 0
  under `HKEY_CURRENT_CONFIG\System\CurrentControlSet\Control\Print\Printers\<queue name>`;
  clearing the setting resets it.
- Follow Microsoft's printer connection troubleshooting for network
  reachability, cabling and driver steps.

## Gotchas
- A single huge or malformed job blocks the jobs behind it; remove that one
  first and retry.
- Restarting the spooler does not fix a printer that is jammed or out of
  memory; check the printer panel.

## Verify
`Get-PrintJob` empty or flowing, spooler service Running, and a test page
prints.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn Windows Server troubleshooting articles (dated February 2026), Microsoft Support printer troubleshooting page, PrintManagement module reference. Confirmed: Get-PrintJob and Remove-PrintJob parameters, Restart-Service and net stop/start spooler, clearing the spool PRINTERS folder, the spooler-not-running checklist, the Use Printer Offline and PrinterOnLine behaviour. Removed: event IDs, driver isolation, print-processor registry advice and SNMP/WSD port tips that no fetched page covers.

Method: documentation only; no commands were run.
