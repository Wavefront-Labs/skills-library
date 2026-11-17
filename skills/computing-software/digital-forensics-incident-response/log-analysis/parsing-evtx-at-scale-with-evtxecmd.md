---
id: computing-software.digital-forensics-incident-response.log-analysis.parsing-evtx-at-scale-with-evtxecmd
name: parsing-evtx-at-scale-with-evtxecmd
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [evtxecmd, evtx, windows-event-logs, kape-modules, dfir]
level: practitioner
status: gated
description: "Parse EVTX logs at scale with EvtxECmd: maps, payload normalisation, VSS and carved record options, CSV/JSON output and loading results into Timeline Explorer or a SIEM."
sources: ["https://github.com/EricZimmerman/evtx", "https://ericzimmerman.github.io/", "https://github.com/EricZimmerman/evtx/tree/master/evtx/Maps"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing EVTX at scale with EvtxECmd

**Goal:** turn hundreds of `.evtx` files from many hosts into one normalised table where the
important fields of each event ID are in consistent columns.

## Run
```cmd
EvtxECmd.exe -d <triage>\C\Windows\System32\winevt\Logs --csv out\ --csvf evtx.csv
EvtxECmd.exe -f Security.evtx --json out\ --inc 4624,4625,4672,4688
EvtxECmd.exe -d logs\ --csv out\ --vss --dedupe              :: include VSS copies on live/mounted volumes
EvtxECmd.exe -f Security.evtx --csv out\ --sd 2026-10-01 --ed 2026-10-14   :: date range
EvtxECmd.exe --sync                                           :: update maps from GitHub
```
- `--inc` / `--exc` event ID filters; `--metrics` prints per-file counts; `--fj` full JSON payload.
- Carved/corrupt files: EvtxECmd recovers records from dirty or partially overwritten logs; for unallocated carving use dedicated carvers first.

## Maps
- YAML maps per Channel + EventID extract fields into `UserName`, `RemoteHost`, `ExecutableInfo`,
  `PayloadData1..6`, so e.g. 4624 logon type and source IP land in fixed columns.
- Write a map for custom/vendor events:
```yaml
Author: IR
Description: Vendor agent alert
EventId: 1001
Channel: Application
Provider: VendorAgent
Maps:
  - Property: PayloadData1
    PropertyValue: "Rule: %Rule%"
    Values:
      - Name: Rule
        Value: "/Event/EventData/Data[@Name=\"RuleName\"]"
```
Drop it in the `Maps` folder (named `Application_VendorAgent_1001.map`).

## Analyse
- Open CSV in Timeline Explorer (handles millions of rows, column filters, grouping).
- Or ship JSON to Elastic/Splunk/Timesketch for multi-host analysis.

## Gotchas
- Event message templates on the analysis host may differ; EvtxECmd works from XML payload, not rendered messages, which is more reliable.
- Time column is UTC.

## Verify
`--metrics` counts per event ID match `Get-WinEvent` counts on a sample file.

## Checked

- Date: 2026-11-02.
- Confirmed against: EvtxECmd options --csv, --csvf, --json, --inc, --sd, --dedupe, --sync and the --vss Windows-only note (EricZimmerman/evtx README).
- Not confirmed: the map XML structure, PayloadData fields and the --metrics flag (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
