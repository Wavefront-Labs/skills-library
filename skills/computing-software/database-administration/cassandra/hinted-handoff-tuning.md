---
id: computing-software.database-administration.cassandra.hinted-handoff-tuning
name: hinted-handoff-tuning
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, hints, max-hint-window, hints-directory, hinted-handoff, read-repair, batchlog, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "How hints behave"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/hints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hinted handoff

Goal: tune hints for brief outages.
- A coordinator stores a hint when a replica is unavailable; hints are kept for up to `max_hint_window` of downtime (default 3 hours), after which repair is needed.
- Runtime commands: `nodetool statushandoff`, `disablehandoff`, `enablehandoff`, `pausehandoff`, `resumehandoff`, `truncatehints`, `setmaxhintwindow` (4.0+), `sethintedhandoffthrottlekb`.
- Related settings: `hinted_handoff_enabled`, `hinted_handoff_throttle` (default 1024KiB), `max_hints_delivery_threads` (default 2), `hints_directory`, `hints_compression` (LZ4 default).
- A long outage can accumulate many gigabytes of hints that take hours to deliver.
Verify: the hints directory drains after the node returns.

## Checked

2026-11-02. Checked against the Hinted Handoff page (max_hint_window default, settings table, nodetool commands, accumulation warning). Removed: 'hints are not a substitute for repair' wording beyond the window rule (kept only the stated window rule).

Method: documentation only; no commands were run.
