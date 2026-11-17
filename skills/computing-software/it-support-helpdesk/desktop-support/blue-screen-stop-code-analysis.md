---
id: computing-software.it-support-helpdesk.desktop-support.blue-screen-stop-code-analysis
name: blue-screen-stop-code-analysis
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, stop-code-analysis, bsod, bugcheck, minidump, windbg, analyze-v, driver-verifier, memory-dmp, boot-failure]
level: advanced
status: docs-checked
description: "Turn a blue screen into a cause: configure and find dumps, run WinDbg !analyze -v, look up stop codes, and use Driver Verifier on a test machine only."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/bug-check-code-reference2"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/stop-error-or-blue-screen-error-troubleshooting"
  - "https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/driver-verifier"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# blue-screen-stop-code-analysis

Goal: name the driver or hardware behind a BSOD from evidence, not by
reinstalling Windows.

## Collect
- Configure dumps: Advanced system settings, Advanced tab, Startup and
  Recovery Settings, "Write debugging information" set to Automatic memory
  dump, OK, then restart. On a virtualised server, disable auto reboot after
  the dump so you can snapshot the machine.
- Where dumps land: small memory dump (256 KB) in `%SystemRoot%\Minidump`;
  kernel, complete, automatic and active dumps in `%SystemRoot%\MEMORY.DMP`.
- DumpChk (Microsoft Crash Dump File Checker) verifies a dump is not corrupt.
- Microsoft estimates about 75 percent of stop errors are caused by faulty
  drivers.

## Analyse
Copy `MEMORY.DMP` to another computer and install Debugging Tools for Windows
(WinDbg) from the Windows SDK. Set the symbol path (File, Symbol File Path) to
the Microsoft symbol server `https://msdl.microsoft.com/download/symbols`
(or a local path when offline), Open Crash Dump, then under Bugcheck Analysis
run `!analyze -v`. Read the STACK_TEXT section: the text should name the DLL
or driver behind the crash. `!analyze -show <code> <param1>` explains a
specific bug check parameter.

## Stop codes
The Bug Check Code Reference is the full code-to-name list. Codes this skill
commonly meets (hex value and name as listed there):

| Code | Name |
|---|---|
| 0xA | IRQL_NOT_LESS_OR_EQUAL |
| 0x1A | MEMORY_MANAGEMENT |
| 0x50 | PAGE_FAULT_IN_NONPAGED_AREA |
| 0x7B | INACCESSIBLE_BOOT_DEVICE |
| 0xD1 | DRIVER_IRQL_NOT_LESS_OR_EQUAL |
| 0xEF | CRITICAL_PROCESS_DIED |
| 0x116 | VIDEO_TDR_FAILURE |
| 0x124 | WHEA_UNCORRECTABLE_ERROR |
| 0x133 | DPC_WATCHDOG_VIOLATION |

Microsoft's troubleshooting page gives these first moves:
- DRIVER_IRQL_NOT_LESS_OR_EQUAL: apply the latest cumulative updates and
  update the driver, often a network driver; for VMware guests use the VMware
  network adapter types (VMXNET family) rather than the Intel PRO/1000 driver.
- PAGE_FAULT_IN_NONPAGED_AREA: contact the vendor for an update of the driver
  named, or disable it; run `chkdsk /f /r` (restart first for a system
  partition); reinstall a recently installed or updated application.
- KMODE_EXCEPTION_NOT_HANDLED (0x1E): disable or remove the named or recently
  added driver; safe mode can be used when it fails at startup.
- NTFS_FILE_SYSTEM (0x24): usually NTFS corruption or bad sectors; run the
  storage vendor's diagnostics and a disk check.
- Missing or corrupt system files: run System File Checker.
- Video TDR timeouts (0x141, 0x117): contact the vendor of the named display
  driver for an update.

## Driver Verifier (test machines only)
The page warns that running it can crash the computer and should only be done
on computers used for testing and debugging; you must be an administrator.
- `verifier /standard /driver myDriver.sys` runs standard settings against one
  driver; `verifier /query` shows statistics, `verifier /querysettings`
  shows settings, `verifier /reset` then a restart stops it.
- Do not verify all drivers at once: Microsoft's troubleshooting page says
  this degrades performance and limits effectiveness. Test suspicious drivers
  (recently updated or known problematic), or third-party and unsigned
  drivers in groups of 10 to 20.
- Violations cause a bug check, typically 0xC4
  (DRIVER_VERIFIER_DETECTED_VIOLATION); use `!analyze -v`, `!verifier`.
- If the machine cannot reach the desktop, start in Safe mode, where the tool
  does not run, and disable it.

## Verify
After the fix, the machine runs without new stop errors, and a fresh dump (if
one occurs) names a different or no driver.

## Checked

Date 2026-11-08. Pages: Microsoft Learn Bug Check Code Reference (code list), the Windows stop error troubleshooting article, and the Driver Verifier article. Confirmed: dump settings and locations, WinDbg and `!analyze -v` steps, the code-to-name pairs above, Driver Verifier commands and warnings, 10 to 20 driver groups, Safe mode disabling. Removed as not on the pages: Event 1001 and Kernel-Power 41 guidance, Get-WinEvent query, page file sizing, `.symfix` and `lmvm`, the per-code cause column for most codes (RAM, PSU, firmware advice), the claim that ntoskrnl.exe on the stack implies earlier corruption, Disk Cleanup and credential-in-dump notes, and the mean-time verification target.

Method: docs-only read of cited pages, 2026-11-08
