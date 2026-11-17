---
id: computing-software.data-engineering.apache-pinot.apache-pinot-hybrid-table-time-boundary
name: apache-pinot-hybrid-table-time-boundary
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, time-boundary, hybrid-table, timeboundary, offline-table, realtime-table]
level: practitioner
status: docs-checked
description: "How the broker splits a hybrid table query at the time boundary (max offline end time minus 1 hour or 1 day) and the REST calls to pin it."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/concepts/time-boundary.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid table time boundary

A hybrid table is an offline and a real-time table with the same name. The broker uses the time boundary to decide which records come from which side. For a query on `events` it sends:
- to `events_OFFLINE`: `WHERE timeColumn <= $timeBoundary`
- to `events_REALTIME`: `WHERE timeColumn > $timeBoundary`

and merges the two results before returning them.

The boundary is derived from the **maximum end time of the offline segments** and the segment ingestion frequency configured for the offline table:
- hourly ingestion frequency: boundary = max offline end time minus 1 hour
- otherwise: boundary = max offline end time minus 1 day

From Pinot 0.12.0 you can force the table to use the plain max(end time of all offline segments) with the controller API:
```
POST   /tables/{tableName}/timeBoundary
DELETE /tables/{tableName}/timeBoundary
```
POST does not keep updating: it must be called again every time a segment with a more recent end time is uploaded to the offline table. DELETE reverts to the derived boundary. Both are called on the controller (the docs example uses port 9000 with `accept: application/json`).

## Checked

2026-11-08. Read the whole pinot-docs time-boundary page. Confirmed the derivation (1 hour for hourly, otherwise 1 day), the version gate 0.12.0+, the POST and DELETE behaviour and the query split. Removed three consequence bullets the page does not state (realtime-to-offline task relying on the overlap, late events visible only offline, "boundary advances when a segment lands" as a guarantee), and corrected POST from a generic "override" to forcing max end time without auto-update.

Method: documentation only; no commands were run.
