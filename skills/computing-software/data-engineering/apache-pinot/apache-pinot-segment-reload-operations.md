---
id: computing-software.data-engineering.apache-pinot.apache-pinot-segment-reload-operations
name: apache-pinot-segment-reload-operations
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, segment-reload, reload, forcedownload, onlyifneeded, targetinstance, instancetosegmentsmap, segmentreloadstatus, index-rebuild]
level: practitioner
status: docs-checked
description: "Reloading Pinot segments: reload endpoint parameters (type, forceDownload, onlyIfNeeded, targetInstance, time range) and job status."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/segment-reload.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Segment reload operations

Reload makes servers rebuild segments with the current table config and schema, for example to add an index or a new column.
```
POST /segments/myTable/reload?type=OFFLINE&forceDownload=false
GET  /segments/segmentReloadStatus/{jobId}
```

Parameters:
- `type`: `OFFLINE` or `REALTIME`.
- `forceDownload`: re-download immutable segments from deep store before reloading (default false; only supported for immutable segments, so a raw table name is limited to OFFLINE).
- `onlyIfNeeded`: skip segments whose loaded copy does not need reload (default false; ignored when `forceDownload=true`).
- `targetInstance`: send reload messages only to that server instance.
- `instanceToSegmentsMap`: explicit segment lists per instance.
- `startTimestamp` / `endTimestamp`: milliseconds since epoch (end exclusive); segments overlapping the window are reloaded, or only fully contained ones with `excludeOverlapping=true`.

The call is asynchronous and returns a job id. Poll `segmentReloadStatus`: the response has `status`, `totalSegmentCount`, `successCount` and `failureCount`.

For consuming segments, reload requests a force commit when `pinot.server.instance.reload.consumingSegment` is true (the default).

## Checked

2026-11-09: confirmed against the Pinot Reload a table segment page (pinot-docs operate-pinot/segment-reload.md): the three controller endpoints, the query parameters and defaults, time-range reload, the job id and status response, and the consuming segment force commit behaviour. Removed the unconfirmed claims about when forceDownload is needed, that reload drops removed indexes, and the advice to slice big tables.

Method: documentation only; no commands were run.
