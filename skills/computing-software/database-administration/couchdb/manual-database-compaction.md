---
id: computing-software.database-administration.couchdb.manual-database-compaction
name: manual-database-compaction
category: computing-software
field: database-administration
product: couchdb
tags: [compaction, manual, active-tasks, compact-running, content-type]
level: practitioner
status: docs-checked
description: "Trigger and monitor manual CouchDB database compaction with POST /{db}/_compact, compact_running in database info, and _active_tasks."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/maintenance/compaction.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start compaction (it runs as a background task):

```
curl -H "Content-Type: application/json" -X POST http://adm:pass@localhost:5984/my_db/_compact
```

Success returns `202 Accepted` with `{"ok":true}` immediately.

The request body is unused, but the `Content-Type: application/json` header is required. Without it you get `415 Unsupported Media Type` with `bad_content_type`.

Monitor:

- `GET /my_db` shows `"compact_running": true` while it runs, plus `sizes` with `active`, `disk` and `external`.
- `GET /_active_tasks` lists a task of `type` `database_compaction` with `changes_done`, `total_changes` and `progress`.

Compaction replaces old revisions with tombstones. How many revisions are retained is set with `/{db}/_revs_limit`.

## Checked

2026-11-04. Confirmed against the CouchDB maintenance/compaction page (Manual Database Compaction): POST _compact, 202 response, Content-Type requirement and 415 bad_content_type, compact_running, sizes, _active_tasks fields. Removed the gloss that progress is a percentage.

Method: documentation only; no commands were run.
