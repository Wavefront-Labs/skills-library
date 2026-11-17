---
id: computing-software.cybersecurity-defensive.splunk.data-model-acceleration
name: data-model-acceleration
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-enterprise-security, data-model-acceleration, cim, tsidx, summary-range, cim-indexes-macro, performance-tuning]
level: advanced
status: draft
description: "Run CIM data model acceleration for Splunk ES: index constraint macros, summary range, backfill, max concurrent, and diagnosing incomplete or lagging summaries."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Acceleratedatamodels", "https://docs.splunk.com/Documentation/ES/latest/Install/Datamodels", "https://docs.splunk.com/Documentation/CIM/latest/User/Setup"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data model acceleration for ES

ES correlation searches and dashboards mostly read accelerated CIM data models via tstats.
If acceleration is broken, detections go quiet without erroring.

## Setup
1. **Constrain indexes**: Settings > Data inputs > CIM Setup (Splunk_SA_CIM) or edit macros
   `cim_Authentication_indexes`, `cim_Endpoint_indexes`, etc. Set e.g. `(index=wineventlog OR index=linux)`.
   Default `index=*`-style constraints scan everything and slow builds.
2. **Enable acceleration** per model with a summary range matching how far back detections and
   dashboards look (Authentication 30d, Network_Traffic 7d is common; longer costs disk and CPU).
3. ES Data Model Audit dashboard (Audit > Data Model Audit) shows size, completion, and run time.

## Key settings (datamodels.conf, Splunk_SA_CIM local)
```
[Network_Traffic]
acceleration = true
acceleration.earliest_time = -7d
acceleration.max_concurrent = 3
acceleration.backfill_time = -1d
acceleration.max_time = 3600
acceleration.manual_rebuilds = false
```
- `backfill_time` shorter than earliest_time builds recent data first after a rebuild.
- `max_time` caps one summarisation run; too low and big indexes never catch up.
- Acceleration searches run on the search head but build tsidx files on indexers.

## Diagnose
- Completion < 100% persistently: summarisation cannot keep up. Check
  `index=_internal sourcetype=scheduler savedsearch_name="_ACCELERATE_DM_*"` for skipped runs and run time.
- Search head concurrency: acceleration jobs share the scheduler; skipped searches in the
  Monitoring Console point to too many concurrent jobs.
- Fields missing in tstats: the data model does not extract them because the sourcetype is not
  CIM-tagged (`tag=authentication` missing). Fix the TA eventtypes/tags.
- Changing a data model definition triggers a full rebuild; schedule it.

## Gotchas
- `summariesonly=true` searches return nothing for ranges not yet summarised.
- Large `Network_Traffic` and `Web` models dominate disk; restrict indexes hard.
- Indexer clusters: summaries are not replicated by default (`summary_replication=false`), so a
  peer outage leaves gaps until rebuilt.

## Verify
`| tstats summariesonly=t count from datamodel=Authentication by _time span=1h` shows no gaps
compared with `summariesonly=f` across the summary range.
