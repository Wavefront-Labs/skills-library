---
id: computing-software.database-administration.couchdb.monitor-replication-scheduler
name: monitor-replication-scheduler
category: computing-software
field: database-administration
product: couchdb
tags: [replication, monitoring, scheduler-jobs, scheduler-docs, backoff]
level: practitioner
status: docs-checked
description: "Check replication health with /_scheduler/docs and /_scheduler/jobs, read info counters and history, and understand scheduler round-robin and backoff."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Replication document contents stay unchanged; state is read from the scheduler (since 2.1).

- `GET /_scheduler/docs/_replicator/my_rep` returns `state`, `error_count`, `last_updated`, `start_time`, and `info` counters: `revisions_checked`, `missing_revisions_found`, `docs_read`, `docs_written`, `changes_pending`, `doc_write_failures`, and the `source_seq`, `through_seq`, `checkpointed_source_seq` markers.
- `GET /_scheduler/jobs` shows running jobs with a detailed `history` of `started`, `added` and `crashed` events (with a `reason`). If a persistent replication has not started, failed or completed, its state is only in `_scheduler/docs`.

Failures: a missing source database makes the job crash and retry after a wait that grows with each consecutive crash (state `crashing`, `info.error` like `db_not_found`). Creating the missing database lets it recover.

The scheduler periodically stops some jobs and starts others, so more jobs than the cluster can run at once are possible. Round-robin: the longest-running jobs stop, the longest-waiting start. Failing jobs wait exponentially longer. Behaviour is set by `max_jobs`, `interval` and `max_churn`.

## Checked

2026-11-04. Confirmed against the CouchDB replication/replicator page (Replication Status, Replication Scheduler): scheduler introduced in 2.1, _scheduler/docs fields and info counters, _scheduler/jobs history with reasons, the crashing state with db_not_found, round-robin and exponential penalty, and the max_jobs, interval and max_churn options. Nothing removed.

Method: documentation only; no commands were run.
