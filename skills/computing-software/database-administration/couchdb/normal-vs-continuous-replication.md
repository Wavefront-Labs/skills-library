---
id: computing-software.database-administration.couchdb.normal-vs-continuous-replication
name: normal-vs-continuous-replication
category: computing-software
field: database-administration
product: couchdb
tags: [replication, continuous, scheduler, compatibility-mode, cancel-replication]
level: practitioner
status: docs-checked
description: "How the scheduler treats normal versus continuous CouchDB replications, starvation risk, compatibility mode, cancelling, updating and restarts."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Normal replications** run to completion once started, to preserve snapshot semantics: documents added to the source after the start should not appear on the target. Stopping and restarting would violate that. Warning: when normal and continuous jobs are mixed, a scheduled normal replication can temporarily starve continuous ones. Normal replications are still stopped and requeued if an operator lowers the maximum number of replications.

**Compatibility mode.** Older versions wrote state back into replication documents. To keep doing so for code that reads it:

```ini
[replicator]
update_docs = true
```

To effectively disable the scheduler's periodic stop/start, set `max_jobs` to a very large number (the page uses 9999999).

**Changing.** `DELETE` the replication document to cancel; update the document (for example workers or source) to change it. Extra application data in the document is ignored.

**Restart.** On restart CouchDB rescans `_replicator` databases and restarts replications not already `completed` or `failed`.

## Checked

2026-11-04. Confirmed against the CouchDB replication/replicator page: normal replication snapshot semantics, starvation warning, requeue when max replications is lowered, compatibility mode update_docs and max_jobs 9999999, DELETE and update to cancel or change, restart behaviour. Nothing removed.

Method: documentation only; no commands were run.
