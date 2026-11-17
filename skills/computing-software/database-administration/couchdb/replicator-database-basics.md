---
id: computing-software.database-administration.couchdb.replicator-database-basics
name: replicator-database-basics
category: computing-software
field: database-administration
product: couchdb
tags: [replication, replicator-database, replication-documents, duplicate-replication, continuous]
level: practitioner
status: docs-checked
description: "Start and stop CouchDB replications by writing and deleting documents in _replicator, extra /_replicator databases, and duplicate document behaviour."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`_replicator` works like any database, but documents added to it trigger replications. `PUT` or `POST` a document to start one; `DELETE` it to cancel. Content matches the `_replicate` body: `source`, `target`, `create_target`, `create_target_params`, `continuous`, `doc_ids`, `filter`, `query_params`, `use_checkpoints`, `checkpoint_interval`. Since 3.3.0, `winning_revs_only: true` replicates only winning revisions.

```json
{
  "_id": "my_rep",
  "source": "http://user:password@myserver.com/foo",
  "target": {"url": "http://localhost:5984/bar",
             "auth": {"basic": {"username": "adm", "password": "pass"}}},
  "create_target": true,
  "continuous": true
}
```

- A user-defined `_id` makes the replication easy to find later.
- Design documents and `_local` documents in a replicator database are ignored.
- Extra replicator databases must have names ending in `/_replicator`.
- Two documents describing the same replication (identical parameters, different `_id`): the first triggers it, the second ends in the terminal `failed` state. Malformed values (for example a string for `worker_processes`) also fail.

## Checked

2026-11-04. Confirmed against the CouchDB replication/replicator page (Replication Database, Basics, Replication states): start and cancel by PUT, POST and DELETE, the listed document fields, user-defined _id, ignored design and _local documents, the /_replicator suffix rule, winning_revs_only (3.3.0), duplicate document ending in terminal failed state. Nothing removed.

Method: documentation only; no commands were run.
