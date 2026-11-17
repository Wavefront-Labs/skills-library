---
id: computing-software.cybersecurity-defensive.splunk.tstats-accelerated-data-model-searches
name: tstats-accelerated-data-model-searches
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, tstats-command, tstats, data-models, cim, summariesonly, datamodel-acceleration, investigation]
level: practitioner
status: draft
description: "Write fast tstats searches over CIM-accelerated data models: nodename syntax, summariesonly, prestats chaining, by _time span, and why results differ from raw search."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Tstats", "https://docs.splunk.com/Documentation/CIM/latest/User/Overview", "https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Acceleratedatamodels"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# tstats over accelerated data models

**Goal:** answer "who/what/how many" across weeks of security data in seconds by reading the
tsidx summaries instead of raw events.

## Core syntax
```
| tstats summariesonly=true allow_old_summaries=true count
    from datamodel=Authentication.Authentication
    where Authentication.action=failure
    by Authentication.src Authentication.user _time span=1h
| rename Authentication.* as *
```
- `from datamodel=<Model>.<root_dataset>`; child nodes: `datamodel=Endpoint.Processes`,
  `nodename=Authentication.Failed_Authentication` for inherited constraints.
- Every field is prefixed with the dataset name; `rename Model.* as *` at the end keeps the
  rest of the pipeline readable.
- Aggregates allowed: `count`, `dc()`, `values()`, `min()`, `max()`, `sum()`, `avg()`,
  `latest()`, `earliest()`. No `eval` inside tstats; do it after.

## Common security patterns
Rare parent-child process pairs:
```
| tstats summariesonly=t count from datamodel=Endpoint.Processes
    by Processes.parent_process_name Processes.process_name
| rename Processes.* as * | where count < 5
```
Brute force then success (two tstats with `prestats=t` and `append=t`):
```
| tstats prestats=t summariesonly=t count from datamodel=Authentication where Authentication.action=failure by Authentication.src
| tstats prestats=t append=t summariesonly=t count from datamodel=Authentication where Authentication.action=success by Authentication.src
| stats count by Authentication.src
```
Raw-index tstats (no data model, indexed fields only): `| tstats count where index=* by index sourcetype host`
is the fastest inventory of what is arriving.

## summariesonly
- `summariesonly=true`: only the accelerated summary; fast, but misses time ranges whose
  summary is still building and any events that do not match the model constraints.
- `false` (default): falls back to raw search for unsummarised ranges; correct but can be slow.
- Detections usually use `true` plus a health check on acceleration completion.

## Gotchas
- Fields not in the data model cannot be used. Check the model in Settings > Data models or
  `| datamodel Authentication Authentication search | head 1`.
- Values that were not CIM-normalised at ingest (e.g. `action=Failed` instead of `failure`)
  silently drop out. Validate with `| tstats count from datamodel=Authentication by Authentication.action`.
- `_time span` must be a multiple of the summary granularity; very small spans over long ranges
  produce huge result sets.
- Data model constraints are index-restricted by the `cim_<Model>_indexes` macro; new indexes
  must be added there or the data never reaches the summary.

## Verify
Run the same question with `summariesonly=false` over a short window and compare counts; a gap
means acceleration lag or a normalisation miss.
