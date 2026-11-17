---
id: computing-software.database-administration.couchdb.replication-job-states
name: replication-job-states
category: computing-software
field: database-administration
product: couchdb
tags: [replication, job-states, crashing, pending, terminal-states]
level: practitioner
status: docs-checked
description: "Meaning of CouchDB replication job states initializing, failed, error, running, pending, crashing and completed, and which are terminal."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page's diagram marks states healthy (blue) or unhealthy (yellow), and terminal (rectangle) or non-terminal (oval). Terminal jobs are not retried and use no CPU or memory.

- **Initializing**: replicator noticed the document change. Should pass quickly; stuck here may mean an internal error.
- **Failed** (terminal): the document could not become a valid job. Typical causes: malformed document (an integer for a boolean parameter) or a duplicate replication (same parameters, different document ID). Needs user intervention.
- **Error** (temporary): update could not be turned into a job; retried with exponential backoff. Exists mainly for filtered replications with custom functions, whose code must be fetched over the network to compute the replication ID.
- **Running**: working normally, even if just waiting on the changes feed. Continuous replications usually sit here.
- **Pending**: waiting its turn because jobs exceed `replicator.max_jobs`; the scheduler rotates subsets.
- **Crashing** (temporary): added, but the last run hit an error (network, missing database, permissions). Retried with exponential backoff.
- **Completed** (terminal): successful end for non-continuous replications. Continuous never reach it.

Maximum backoff for Error and Crashing derives from `replicator.max_history`.

## Checked

2026-11-04. Confirmed against the CouchDB replication/replicator page (Replication states): colour and shape meanings, all seven state descriptions, terminal states, max_jobs, max_history backoff note. Nothing removed.

Method: documentation only; no commands were run.
