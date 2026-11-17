---
id: computing-software.cybersecurity-defensive.security-operations.procmon-regshot-behavioural-analysis
name: procmon-regshot-behavioural-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [procmon-analysis, malware-analysis, dynamic-analysis, process-monitor, regshot, sysinternals, behavioural-analysis]
level: practitioner
status: draft
description: "Perform dynamic malware behavioural analysis with Process Monitor, Regshot and Process Explorer: filters, capturing persistence, file and registry changes, and reporting."
sources: ["https://learn.microsoft.com/en-us/sysinternals/downloads/procmon", "https://github.com/Seabreg/Regshot", "https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Behavioural analysis with Procmon and Regshot

Run only in an isolated analysis VM (snapshot, host-only networking or simulated internet).

## Preparation
1. Revert VM to clean snapshot; disable Defender realtime protection in the VM if the sample must run.
2. Start Regshot: **1st shot** (scan registry and optionally the file system, e.g. `%SystemDrive%\`).
3. Start Process Monitor; clear the log; set filters before running the sample:
   - `Process Name is sample.exe` include, plus `Operation is Process Create` include to follow children.
   - Or use Process Tree later and filter by PID set.
   - Exclude noise: `Process Name is procmon64.exe/Explorer.EXE/System` exclude.
4. Start Process Explorer (verify signatures, VirusTotal column optional offline), FakeNet-NG or INetSim
   for network.

## Run and capture
Execute the sample, interact if needed (documents need enabling macros), wait several minutes
(some samples sleep), then stop capture, take Regshot **2nd shot** and **Compare**.

## What to extract
- **Persistence**: `RegSetValue` under `HKCU\...\Run`, `RunOnce`, services (`HKLM\SYSTEM\CurrentControlSet\Services`),
  scheduled tasks (files under `System32\Tasks`), WMI subscriptions, startup folder.
- **Dropped files**: `WriteFile`/`CreateFile` with disposition create in `%AppData%`, `%Temp%`,
  `ProgramData`; collect them for further analysis.
- **Process injection hints**: child processes started suspended, writes into other processes
  (better seen with API monitors/EDR).
- **Discovery/defence evasion**: queries of VM artefacts (`VBox`, `vmware` registry keys), security
  product registry keys, deleting shadow copies (`vssadmin delete shadows`).
- Procmon Tools > Process Tree and File Summary / Registry Summary for overview.

## Report
Indicators (files with hashes, registry keys, mutexes, network), behaviours mapped to ATT&CK, and
screenshots of the process tree.

## Gotchas
- Anti-analysis: samples detect Procmon/VMs; rename tools, use hardened VMs, or rely on sandbox
  with bare-metal options.
- Regshot misses short-lived changes that are later reverted; Procmon catches them.

## Verify
Indicators extracted reproduce when the sample is rerun on a fresh snapshot.
