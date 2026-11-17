---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.process-explorer-autoruns-and-log-bundles
name: process-explorer-autoruns-and-log-bundles
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, process-explorer-analysis, autoruns-persistence, log-bundle, sysinternals, evidence-gathering, diagnostics]
level: practitioner
status: draft
description: "Gather evidence with Sysinternals Process Explorer and Autoruns, and collect the right application and OS diagnostic log bundles for escalation and vendor cases."
sources:
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer"
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/autoruns"
  - "https://learn.microsoft.com/en-us/microsoft-365/troubleshoot/diagnostic-logs/collect-logs-with-microsoft-support-and-recovery-assistant"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# process-explorer-autoruns-and-log-bundles

## Process Explorer
- Run as admin; replace Task Manager optionally. Tree view shows parent/child: an
  `outlook.exe` spawning `powershell.exe` is suspicious.
- Columns worth adding: Command Line, Verified Signer, Company Name, CPU History, Private
  Bytes, Handles, GPU.
- Options > **VirusTotal.com** > Check VirusTotal.com: flags known-bad hashes (uploads
  hashes only unless you choose to submit files).
- **Find > Find Handle or DLL** (Ctrl+F): which process has a file locked.
- Process properties: Threads (stack of a hung thread), TCP/IP (connections), Strings,
  Image (path, autostart location).
- Create dump: right-click > Create Dump > Full dump for vendor analysis.

## Autoruns
- Shows every autostart location: Logon (Run keys, Startup folder), Scheduled Tasks,
  Services, Drivers, Explorer and browser add-ons, WMI, Winlogon, Image hijacks, KnownDLLs.
- Options: **Hide Microsoft entries** and **Hide Windows entries**; enable **Verify code
  signatures** and VirusTotal. Yellow rows = target file missing; pink = unsigned/no
  publisher.
- Untick to disable (reversible) rather than delete while testing.
- Compare against a clean baseline: File > Save on a known-good machine, then File >
  Compare.
- `autorunsc -a * -c -h -s -m > autoruns.csv` (command line, CSV, hashes, signatures,
  hide Microsoft) for remote collection.
- Persistence found during malware work: preserve evidence and follow the security
  handoff before removing.

## Log bundles for escalation
| Area | Tool / bundle |
|---|---|
| Microsoft 365 apps (Outlook, Teams) | Get Help app / Microsoft Support and Recovery Assistant (SaRA enterprise command line) |
| Teams | Ctrl+Alt+Shift+1 (new Teams) downloads diagnostic logs |
| Intune / MDM | Collect diagnostics remote action, MDM diagnostic report (`mdmdiagnosticstool.exe -area DeviceEnrollment;DeviceProvisioning -zip <OUTPUT_DIR>\mdm.zip`) |
| Windows Update | `Get-WindowsUpdateLog` |
| General Windows | `msinfo32 /nfo`, Event logs exported as .evtx, `dxdiag /t` |
| macOS | `sudo sysdiagnose` |
| Vendor apps | Vendor's "collect logs" option (VPN clients, backup agents) |
- Name bundles with ticket number and device; note the time the issue was reproduced so
  engineers can find it in the logs.
- Scrub or protect: bundles contain usernames, hostnames, sometimes tokens; share via
  the vendor's secure upload, not email.

## Verify
The escalation contains a reproduced timestamp and the right bundle; suspicious processes
or autoruns are documented with signer and path.
