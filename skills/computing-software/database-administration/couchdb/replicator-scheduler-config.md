---
id: computing-software.database-administration.couchdb.replicator-scheduler-config
name: replicator-scheduler-config
category: computing-software
field: database-administration
product: couchdb
tags: [replication, scheduler, max-jobs, max-churn, update-docs]
level: advanced
status: docs-checked
description: "Tune the CouchDB replication scheduler with max_jobs, interval, max_churn, max_history and update_docs in the [replicator] section."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/config/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The scheduler checks every `interval` milliseconds how many replication jobs run. If more than `max_jobs` are active, it pauses and restarts up to `max_churn` jobs from the queue.

```ini
[replicator]
max_jobs = 500
interval = 60000
max_churn = 20
max_history = 20
update_docs = false
```

- `max_jobs` (2.1): too high can cause performance problems; too low means jobs may not progress before being unscheduled. Adjustable at runtime, effective next cycle.
- `interval` (2.1): scheduling interval in ms.
- `max_churn` (2.1): jobs started and stopped per cycle. With `interval` it sets the rate of job replacement. At startup up to `max_jobs` may start quickly.
- `max_history`: events recorded per job; bounds the consecutive failure count and so the maximum backoff before restart.
- `update_docs` (2.1): when `true`, replication documents get error and triggered states, approximating pre-2.1 behaviour.

## Checked

2026-11-04. Confirmed against the CouchDB config/replicator page ([replicator] max_jobs, interval, max_churn, max_history, update_docs): scheduler behaviour description, example values, 2.1 version notes, runtime adjustability, startup burst, max_history backoff bound, update_docs effect. Nothing removed.

Method: documentation only; no commands were run.
