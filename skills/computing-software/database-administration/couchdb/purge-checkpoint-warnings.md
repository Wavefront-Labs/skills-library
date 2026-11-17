---
id: computing-software.database-administration.couchdb.purge-checkpoint-warnings
name: purge-checkpoint-warnings
category: computing-software
field: database-administration
product: couchdb
tags: [purge, checkpoints, local-docs, log-warnings, troubleshooting]
level: advanced
status: docs-checked
description: "Find CouchDB local purge checkpoint documents and respond to the stalled-checkpoint and invalid purge doc log warnings."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/cluster/purging.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Indexes and internal replication write local checkpoint documents `_local/purge-{type}-{hash}` recording the last processed `purge_seq` and a timestamp. They only show in `_local_docs` with `include_system=true`:

```
/test-db/_local_docs?include_system=true
```

A view checkpoint also carries `type` (`mrview`), `ddoc_id` and `signature`.

**Stalled client warning.** During compaction, a client may lag the shard's `purge_seq` by up to `purged_infos_limit + allowed_purge_seq_lag`. If it lags further and has not checkpointed within `index_lag_warn_seconds`, it blocks compaction of the purge trees and a warning like "Purge checkpoint '_local/purge-mrview-...' not updated in 86400 seconds in ..." is logged. Investigate why that index or replication job is not processing purge requests.

**Invalid purge doc warning.** A checkpoint should be deleted automatically when its design document is updated or deleted. If one lingers you see "Invalid purge doc '<<"_design/bar">>' on database ... with purge_seq '50'". Remove that local purge doc from the database.

## Checked

2026-11-04. Confirmed against the CouchDB cluster/purging page (Local Purge Checkpoint Documents and the warnings): _local/purge-{type}-{hash} naming, _local_docs with include_system=true, mrview fields, the stalled-checkpoint warning and the lag formula, the invalid purge doc warning and remedy. Nothing removed.

Method: documentation only; no commands were run.
