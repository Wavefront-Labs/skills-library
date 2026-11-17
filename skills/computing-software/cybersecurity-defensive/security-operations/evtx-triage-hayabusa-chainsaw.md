---
id: computing-software.cybersecurity-defensive.security-operations.evtx-triage-hayabusa-chainsaw
name: evtx-triage-hayabusa-chainsaw
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, hayabusa, chainsaw, evtx, sigma, windows-event-logs, fast-forensics, timeline-analysis]
level: practitioner
status: docs-checked
description: "Triage collected Windows event logs fast with Hayabusa and Chainsaw: Sigma-based detection timelines, logon summaries, search, output to Timesketch, and avoiding false confidence."
sources: ["https://github.com/Yamato-Security/hayabusa", "https://github.com/WithSecureLabs/chainsaw", "https://github.com/SigmaHQ/sigma"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EVTX triage with Hayabusa and Chainsaw

When you have a folder of `.evtx` files from a triage collection (KAPE, Velociraptor) and no SIEM
copy, these tools run thousands of Sigma rules offline in minutes.

## Hayabusa
```
hayabusa update-rules
hayabusa csv-timeline -d ./evtx -o timeline.csv -p super-verbose -m low
hayabusa json-timeline -d ./evtx -L -o timeline.jsonl        # JSONL for Timesketch/Elastic
hayabusa logon-summary -d ./evtx -o logons
hayabusa eid-metrics -d ./evtx                                # event ID counts and percentages
hayabusa search -d ./evtx -k "mimikatz" -k "sekurlsa"
```
- `-m` sets the minimum rule level to load (default informational, so raising it cuts noise). `-p` selects the output profile (`super-verbose` includes all fields and gives larger files).
- `-U` outputs UTC (default is local time). Use consistent UTC across all artefacts in a case.
- Live host scanning (`-l`, local winevt Logs folder) is possible but prefer collected logs to avoid changing the system.
- Other subcommands: `computer-metrics`, `log-metrics`, `eid-metrics`.

## Chainsaw
```
chainsaw hunt ./evtx -s sigma/rules --mapping mappings/sigma-event-logs-all.yml -r rules/ --csv --output out/
chainsaw search "4624" ./evtx --json
chainsaw search -t 'Event.System.EventID: =4104' ./evtx       # tau expressions on fields
chainsaw analyse shimcache SYSTEM --amcache Amcache.hve        # shimcache/amcache timeline
chainsaw analyse srum --software SOFTWARE SRUDB.dat
```
- Chainsaw's own `rules/` directory (Chainsaw rule format, used alongside Sigma) covers AV alerts (Defender, F-Secure, Sophos, Kaspersky), event logs cleared or the event log service stopped, user creation or sensitive-group additions, remote logins (service, RDP, network) and local-account brute force.
- `chainsaw analyse gaps` looks for per-channel EventRecordID holes, a sign of record-level log tampering that does not raise the 1102 event.

## Reading results
1. Sort by level (critical/high first), then build a timeline around each hit +/- 30 minutes.
2. Check the logon summary for unusual source IPs, type 10 (RDP) and type 3 at odd hours,
   failed logon bursts, and explicit credential use (4648).
3. Confirm key detections against raw events (Event Viewer or EvtxECmd output) before reporting.

## Gaps to state in your report
- The 4688 command line field is empty unless the "Include command line in process creation events" policy is
  enabled; without Sysmon or 4688 with command line, many rules cannot fire.
- Logs roll over: check the oldest event per channel (`hayabusa log-metrics`/`eid-metrics`).
- Log clearing (1102) is itself evidence.

## Gotchas
- Rule updates change results; record the rules version (commit hash) used in case notes.
- Sigma rules for generic behaviour produce benign hits (admin tools); triage, do not paste raw output.
- Large datasets: run per host and merge.

## Verify
Seed a test EVTX (e.g. from EVTX-ATTACK-SAMPLES) through the same command line and confirm the
expected detections appear before relying on a clean result.

## Checked
Checked 2026-11-08 against the Hayabusa repository OLD-README (subcommands, `-d -o -p -m -L -U -l -k`, `super-verbose`,
default minimum level), the Chainsaw README (hunt/search/analyse syntax, `--sigma`, `--mapping`, `-r`, `--csv`, tau
`-t`, shimcache `--amcache`, srum `--software`, gaps, built-in rules list) and the Microsoft Learn 4688 page. Fixed:
`hayabusa metrics` (not a subcommand; now `eid-metrics`/`log-metrics`), the Chainsaw rule list (no AV-disabled rule
stated). Removed as unconfirmed: the 20 MB Security log size, event 104, hayabusa RAM remark, the claim that
informational level is very noisy. Levels informational, low, medium, high, critical confirmed.
Method: documentation only; no commands were run.
