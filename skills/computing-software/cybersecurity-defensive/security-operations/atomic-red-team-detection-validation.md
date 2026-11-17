---
id: computing-software.cybersecurity-defensive.security-operations.atomic-red-team-detection-validation
name: atomic-red-team-detection-validation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-as-code, atomic-test-validation, invoke-atomicredteam, detection-testing, purple-team, mitre-attack, test-lab]
level: practitioner
status: draft
description: "Validate detections by running Atomic Red Team tests in a lab: Invoke-AtomicTest usage, prerequisites and cleanup, mapping tests to rules, and recording pass/fail."
sources: ["https://github.com/redcanaryco/atomic-red-team", "https://github.com/redcanaryco/invoke-atomicredteam/wiki", "https://atomicredteam.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Validating detections with Atomic Red Team

Atomic Red Team is a library of small, ATT&CK-mapped tests. Running the test that matches a
detection proves the telemetry arrives and the rule fires. Defensive use: run in a lab or on an
approved test host with change approval, never on production servers ad hoc.

## Install (test host only)
```powershell
IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1' -UseBasicParsing)
Install-AtomicRedTeam -getAtomics
```
EDR/AV will flag the atomics folder; use a dedicated lab machine with an exclusion only for the
atomics directory, and keep detection (not prevention) visibility on.

## Run a test
```powershell
Invoke-AtomicTest T1003.001 -ShowDetailsBrief        # list tests for LSASS dumping
Invoke-AtomicTest T1003.001 -TestNumbers 1 -CheckPrereqs
Invoke-AtomicTest T1003.001 -TestNumbers 1 -GetPrereqs
Invoke-AtomicTest T1003.001 -TestNumbers 1           # execute
Invoke-AtomicTest T1003.001 -TestNumbers 1 -Cleanup
```
- `-TestGuids` pins a specific test across library updates (numbers can shift).
- `-ExecutionLogPath` writes a CSV of what ran and when: the correlation key for your SIEM search.
- Linux/macOS: tests run via `pwsh` with the same module, or execute the YAML commands manually.

## Map tests to detections
Keep a table in the detection repo: rule ID, ATT&CK technique, atomic test GUID, expected alert
name, telemetry source. Each rule should have at least one positive test (and ideally a
benign-but-similar negative case).

## Record results
For each test: executed at (from the execution log), telemetry present (yes/no, which source),
alert fired (yes/no, latency), notes. Common failures:
- No telemetry: audit policy, Sysmon config or EDR data source missing.
- Telemetry but no alert: rule logic or field mapping wrong, or the rule's schedule window missed it.
- Alert fired late: indexing lag; adjust rule look-back.

## Automate
Schedule a weekly run of a fixed test set in the lab and compare alert outcomes with the expected
table (a regression suite for detections). Tools such as Atomic Operator or a CI runner on a lab VM
can drive it.

## Gotchas
- Some tests change system settings or need reboots; always run `-Cleanup`, and use snapshots.
- Tests prove one procedure, not the whole technique; vary procedures before claiming coverage.

## Verify
The execution log timestamp and the alert timestamp line up, and cleanup leaves no artefacts
(re-run `-CheckPrereqs` and inspect the host).
