---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.filer-meta-tail-change-capture
name: filer-meta-tail-change-capture
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [subscribe-metadata, inotify, event-stream, meta-tail, change-data-capture]
level: practitioner
status: docs-checked
description: "Watch filer metadata changes like inotify with weed filer.meta.tail (filters, jq, Elasticsearch) and the SubscribeMetadata gRPC stream."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Filer-Change-Data-Capture
  - https://github.com/seaweedfs/seaweedfs/wiki/Filer-Metadata-Events
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# filer meta tail change capture

```bash
weed filer.meta.tail -timeAgo=3h | jq .eventNotification.newEntry
weed filer.meta.tail -filer=localhost:8888 -pathPrefix=/buckets/photos -pattern="*.pdf"
weed filer.meta.tail -es=http://localhost:9200
```
Flags: `-filer` (default localhost:8888), `-pathPrefix`, `-pattern` (Go filepath.Match style on full path or name), `-timeAgo` (e.g. 300ms, 1.5h, 2h45m), `-es` and `-es.index` (default `seaweedfs`) to push into Elasticsearch.

It calls a gRPC stream API, `SeaweedFiler.SubscribeMetadata(client_name, path_prefix, since_ns)`, which returns `{directory, event_notification{old_entry, new_entry, delete_chunks, new_parent_path}, ts_ns}`. The same stream drives mount metadata sync, async backup, cross-cluster sync and peer filers.

Events are also persisted under `/topics/.system/log` as `yyyy-MM-dd/hh-mm.segment` files of repeated records (4-byte length, then a protobuf `LogEntry`), readable as plain files.

Verify: create a file via the filer and watch the event appear with `newEntry` set.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Filer Change Data Capture and Filer Metadata Events (raw markdown, both read in full).
