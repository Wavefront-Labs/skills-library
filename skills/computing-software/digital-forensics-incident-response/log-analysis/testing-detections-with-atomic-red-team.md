---
id: computing-software.digital-forensics-incident-response.log-analysis.testing-detections-with-atomic-red-team
name: testing-detections-with-atomic-red-team
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [atomic-red-team, detection-testing, invoke-atomicredteam, purple-team, mitre-attack, detection-validation, dfir]
level: practitioner
status: draft
description: "Validate detections and logging coverage with Atomic Red Team tests via Invoke-AtomicRedTeam: safe lab setup, running and cleaning tests, measuring results."
sources: ["https://github.com/redcanaryco/atomic-red-team", "https://github.com/redcanaryco/invoke-atomicredteam/wiki", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing detections with Atomic Red Team

**Goal:** prove that a detection or logging configuration fires on the behaviour it targets,
using small, documented, ATT&CK-mapped tests, before an incident proves otherwise.

## Setup (test system, not production)
```powershell
IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1' -UseBasicParsing)
Install-AtomicRedTeam -getAtomics -Force
Import-Module "$HOME\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1"
```
Run on a dedicated, snapshotted test endpoint enrolled in the same EDR/Sysmon/SIEM pipeline as
production, with change approval and the SOC informed (some tests create users, disable
defences or touch LSASS). Antivirus may block parts of the atomics folder; use exclusions only on
the test host.

## Running tests
```powershell
Invoke-AtomicTest T1059.001 -ShowDetailsBrief           # list tests for PowerShell
Invoke-AtomicTest T1059.001 -TestNumbers 1 -ShowDetails # full commands, inputs, cleanup
Invoke-AtomicTest T1059.001 -TestNumbers 1 -CheckPrereqs
Invoke-AtomicTest T1059.001 -TestNumbers 1 -GetPrereqs
Invoke-AtomicTest T1059.001 -TestNumbers 1               # execute
Invoke-AtomicTest T1059.001 -TestNumbers 1 -Cleanup      # undo
Invoke-AtomicTest T1053.005 -TestNumbers 1 -InputArgs @{ "task_command" = "calc.exe" }   # override an input argument
```
Linux/macOS tests run with PowerShell Core or by copying commands from the YAML (`atomics/T*/T*.yaml`).

## Measuring
For each test record: technique, test number, execution time (UTC), host, expected telemetry
(e.g. Sysmon 1 with `-enc`, 4688, EDR alert name), what arrived in the SIEM, which detection
fired, latency, and gaps. Use the execution log (`Invoke-AtomicTest ... -LoggingModule Attire-ExecutionLogger`)
for exact timestamps.

## Interpreting
- **Telemetry missing:** logging gap (audit policy, Sysmon config, agent not forwarding).
- **Telemetry present, no alert:** detection gap; write or tune the rule (Sigma -> SIEM), retest.
- **Alert fired:** check the alert contains enough context (command line, user, parent) for
  triage.
- Atomic tests are deliberately simple; a passing test does not prove detection of real-world
  variants. Add variations (renamed binaries, different parents, obfuscation) and consider
  emulation frameworks (Caldera, VECTR for tracking).

## Self-check
Each tested detection has a recorded test run, the telemetry observed, pass/fail, and a follow-up
ticket for each gap; cleanup ran on the test host.
