---
id: computing-software.data-engineering.apache-pinot.apache-pinot-realtime-segment-flush-thresholds
name: apache-pinot-realtime-segment-flush-thresholds
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, segment-threshold, flush-threshold, realtime-segment-flush-threshold-rows, realtime-segment-flush-threshold-time, realtime-segment-flush-threshold-segment-size, consuming-segment]
level: practitioner
status: docs-checked
description: "Tuning when a Pinot consuming segment commits: rows, time and segment-size thresholds, rows=0 autotune, and small versus large segments."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/concepts/segment-threshold.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/operate-pinot/tuning/realtime.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/reference/configuration-reference/table.md", "https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/ingestion/stream-ingestion/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Realtime segment flush thresholds

A consuming segment is committed (flushed) when the first applicable end criterion is met. The keys sit in the stream config map of the realtime table (`ingestionConfig.streamIngestionConfig.streamConfigMaps`):

- `realtime.segment.flush.threshold.rows` - table-level rows budget; when `> 0` it has highest precedence and each consuming segment on a server gets roughly rows divided by the partitions that server consumes. `0` (or unset) selects size-based autotune.
- `realtime.segment.flush.threshold.segment.rows` - fixed per-segment rows, used when table-level rows is not positive.
- `realtime.segment.flush.threshold.time` - maximum consuming time, e.g. `24h`. Always set it as a safety net, smaller than the stream retention.
- `realtime.segment.flush.threshold.segment.size` - desired completed-segment size. Only effective when rows is `0`; the controller converts it to a rows threshold using sizes of earlier completed segments. Default `200M` when size-based mode is active and size is unset.
- `realtime.segment.flush.autotune.initialRows` - first segment's rows in autotune mode, default 100,000. Several segment completions may be needed before sizes settle.
- With none of these set, the fallback is 5,000,000 rows at table level.

Recommended starting point:
```
"realtime.segment.flush.threshold.rows": "0",
"realtime.segment.flush.threshold.time": "24h",
"realtime.segment.flush.threshold.segment.size": "200M"
```
Use `pinot-admin.sh RealtimeProvisioningHelper` (with a sample segment) to choose size and hours for your host memory.

Tradeoffs:
- Too small: more segments, more per-query overhead (threads, metadata), more pressure on Helix.
- Too large: servers can run out of memory, and after a restart the consuming segment restarts from its first row, creating lag behind the stream.

Gotcha: with multiple stream configs on one table, all flush settings must match across entries.

## Checked

2026-11-09. Read the Pinot docs pages `segment-threshold.md` and `operate-pinot/tuning/realtime.md` (flush threshold precedence section), plus the table config reference note (partial read) and, by search only, the stream-ingestion README for the multi-stream rule. Confirmed the precedence table, defaults (200M, 100,000, 5,000,000), the safety-net advice, the helper tool and the tradeoffs. Removed: the claim that 24h is the time default (docs only use it as an example value), the Kinesis size-threshold gotcha (not stated in these pages) and the old "50M" example (replaced by the documented recommendation).
Method: documentation only; no commands were run.
