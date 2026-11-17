---
id: computing-software.digital-forensics-incident-response.log-analysis.edr-process-tree-investigation
name: edr-process-tree-investigation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [edr-process-tree, edr, process-tree, crowdstrike, defender-for-endpoint, sentinelone, dfir]
level: practitioner
status: draft
description: "Investigate an alert through the EDR process tree: ancestry, command lines, signer and prevalence, network and file events per process, and scoping across the fleet."
sources: ["https://learn.microsoft.com/en-us/defender-endpoint/investigate-alerts", "https://www.sans.org/posters/hunt-evil/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EDR process tree investigation

**Goal:** from one alert, reconstruct the full execution chain and its effects, then find
the same activity elsewhere.

## Read the tree
1. **Go up** to the root cause: what launched the alerting process? Typical malicious
   chains: `outlook.exe -> winword.exe -> cmd.exe -> powershell.exe`, `w3wp.exe -> cmd.exe`,
   `explorer.exe -> mshta.exe` (from LNK/ISO), `services.exe -> random.exe` (PsExec-style),
   `wmiprvse.exe -> powershell.exe` (WMI remote).
2. **Go down**: all children and grandchildren, including short-lived ones.
3. For each process record: image path, hash, signer, command line, user/integrity, start
   time, parent, and global **prevalence** (how many hosts have this hash/command line).

## Per-process side effects
Network connections (destination, domain, bytes), file writes (dropped binaries, archives),
registry changes (Run keys, services), image loads (unsigned DLLs), injections (cross-process
handles, remote threads), DNS requests.

## Scope
Pivot on hash, command-line fragment, domain, or file path across all endpoints:
```kusto
DeviceProcessEvents
| where Timestamp > ago(30d)
| where ProcessCommandLine has "-enc" and InitiatingProcessFileName in~ ("winword.exe","excel.exe")
| summarize count(), Hosts = dcount(DeviceName) by ProcessCommandLine
```
CrowdStrike Event Search / Falcon LogScale, SentinelOne Deep Visibility (S1QL) offer the same
pivots.

## Gotchas
- Process trees can be broken by PPID spoofing, process hollowing, or long-lived parents
  (explorer.exe); check the creator process separately where the EDR records it.
- Telemetry retention (often 7-30 days) is shorter than dwell time; export early.

## Verify
Write the chain as a short narrative with times; each step cites an EDR event ID or record,
and the scoping query results are saved to the case.
