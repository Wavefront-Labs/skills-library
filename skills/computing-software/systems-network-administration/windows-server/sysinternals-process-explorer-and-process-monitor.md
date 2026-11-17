---
id: computing-software.systems-network-administration.windows-server.sysinternals-process-explorer-and-process-monitor
name: sysinternals-process-explorer-and-process-monitor
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, performance-monitoring, process-monitor, process-explorer, sysinternals, procmon]
level: practitioner
status: draft
description: "Troubleshoot servers with Sysinternals Process Explorer and Process Monitor: find handles, DLLs and CPU threads, capture file/registry activity with filters and boot logging."
sources:
  - https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer
  - https://learn.microsoft.com/en-us/sysinternals/downloads/procmon
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Process Explorer and Process Monitor

Run from `\\live.sysinternals.com\tools` or a copied, signature-checked toolkit. Both need admin for full detail.

## Process Explorer (what is running and why)
- Tree view shows parent/child: services under `services.exe`, scheduled tasks under `svchost.exe` (Schedule).
- **Find > Find Handle or DLL** (Ctrl+F): who has `report.xlsx` open, which process loaded `badfilter.dll`.
- Process > Properties > **Threads**: CPU per thread with stack (configure symbols:
  `srv*<SYMBOLS>*https://msdl.microsoft.com/download/symbols`) to see which module burns CPU.
- **Services** tab inside svchost processes; **TCP/IP** tab for connections.
- Options > VirusTotal check for unknown binaries; column "Verified Signer".

## Process Monitor (what is it doing)
- Captures file system, registry, process/thread and network events live. Huge volume: filter early.
- Typical filters (Ctrl+L): `Process Name is app.exe`, `Result is ACCESS DENIED`, `Result is NAME NOT FOUND`,
  `Path contains \Services\MyApp`.
- Tools > Process Tree, File Summary, Registry Summary for overview.
- Backing file: File > Backing Files > use a file on a data volume, not page file, for long captures.

Command line for remote/short captures:
```cmd
procmon.exe /AcceptEula /Quiet /Minimized /BackingFile <LOGS>\cap.pml
REM reproduce
procmon.exe /Terminate
procmon.exe /OpenLog <LOGS>\cap.pml /SaveAs <LOGS>\cap.csv
```

## Boot logging
Options > Enable Boot Logging, reboot, run procmon again to save the boot log: slow boot and failing services.

## Typical finds
- App fails silently: ACCESS DENIED on a folder/registry key for the service account.
- Slow start: thousands of NAME NOT FOUND probes on a slow network path.

## Verify
- [ ] Root cause found in the capture is confirmed by fixing it (ACL change, path) and re-running the test.
