---
id: computing-software.general-digital-literacy.basic-troubleshooting.clearing-a-stuck-print-queue
name: clearing-a-stuck-print-queue
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, printer, print-queue, stuck-print-job, print-spooler, cancel-print-job, printer-not-printing]
level: intro
status: docs-checked
description: "Cancel stuck print jobs and restart or clear the Windows Print Spooler when one job blocks the queue, and cancel a job on a Mac from the Dock printer icon."
sources:
  - https://support.microsoft.com/en-us/windows/hardware/printer/fix-print-job-stuck-in-queue-errors-in-windows
  - https://support.microsoft.com/en-us/windows/hardware/printer/fix-printer-connection-and-printing-problems-in-windows
  - https://support.apple.com/guide/mac-help/print-documents-mh35838/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clearing a stuck print queue

**Goal:** remove the job that's blocking everything and print again.

## Windows
1. Settings > Bluetooth & devices > **Printers & scanners** > your printer > **Open print queue**.
2. Right-click each job > **Cancel** (on Windows 11 the ... menu also offers **Cancel all**).
3. Jobs won't clear: restart the spooler. Press `Win+R`, type `services.msc`, press Enter, find **Print Spooler**, right-click > **Restart**.
4. Still stuck: clear the spool folder. This deletes every waiting job, so you will need to print them again.
   - In Services, right-click **Print Spooler** > **Stop**.
   - Open File Explorer, go to `%WINDIR%\System32\spool\PRINTERS` and delete all files in that folder.
   - Back in Services, right-click **Print Spooler** > **Start**. (Microsoft's general printer article also sets the spooler's *Startup Type* to **Automatic** when restarting it.)
5. Turn the printer off, wait at least 60 seconds, turn it on, restart the PC, then print again.
6. Windows 11 users can also run the printer troubleshooter in the Get Help app.

## Mac
While a job is printing, click the printer icon that appears in the Dock; you can pause or cancel print jobs from there.

## Verify
- [ ] The queue is empty and a test page prints.

## Checked
Checked 2026-10-27 against Microsoft Support "Fix print job stuck in queue errors in Windows" and "Fix printer connection and printing problems in Windows" (Windows 11 and 10 sections) and the Apple Mac User Guide "Print documents on your Mac". Confirmed: Settings path, Open print queue, Cancel and Cancel all, Print Spooler Restart/Stop/Start in Services, the spool folder location, 60-second printer wait, Dock printer icon. Removed unconfirmed claims (net stop commands, admin requirement, "Deleting - Printing" message, Mac queue window, Resume and Reset printing system, causes of stuck jobs).
Method: documentation only; no commands were run.
