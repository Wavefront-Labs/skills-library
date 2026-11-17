---
id: computing-software.data-engineering.apache-pinot.apache-pinot-segment-retention-policy
name: apache-pinot-segment-retention-policy
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, retention, retentionmanager, retentiontimeunit, retentiontimevalue, segmentingestiontype, refresh, deleted-segments, enablecreationtimefallback]
level: practitioner
status: docs-checked
description: "How Pinot purges old segments: the 6-hour RetentionManager cycle, never-purged segments, creation-time fallback, deleted-segment retention."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/concepts/segment-retention.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Segment retention policy

Segments have a retention time after which they are deleted; offline tables typically retain segments longer than real-time tables. If the retention period is not specified, segments are not purged.

The retention manager does the removal and by default runs once every **6 hours**. It purges:
- expired segments: end time has exceeded the retention period
- replaced segments: replaced by the merge rollup task

Offline-table segments that are not purged:
- a segment with no end time (for example, no time column)
- any segment of a table whose `segmentIngestionType` is `REFRESH`

Invalid or missing end time: by default the retention manager skips such a segment and it is never deleted. Set `controller.retentionManager.enableCreationTimeFallback` to `true` in the cluster configuration to use the segment creation time as the fallback. This setting is dynamic; no controller restart is needed.

Deleted segments first move to a Deleted Segments area and are removed permanently later. The duration is `controller.deleted.segments.retentionInDays` (default **7** days).

When deleting a table via the API, `retention` overrides this: `DELETE /tables/{tableName}?retention=0d` deletes all segments immediately without moving them to the deleted-segments area.

## Checked

2026-11-08. Read the whole pinot-docs segment-retention page. Confirmed the 6-hour default, purged segment types, exceptions, the creation-time fallback and its dynamic nature, the 7-day deleted-segments default and the retention=0d table delete. Removed the `segmentsConfig` field-name sentence and the backfill gotcha, neither stated on the page; added replaced segments.

Method: documentation only; no commands were run.
