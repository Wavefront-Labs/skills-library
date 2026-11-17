---
id: computing-software.database-administration.couchdb.replication-in-a-cluster
name: replication-in-a-cluster
category: computing-software
field: database-administration
product: couchdb
tags: [replication, cluster, failover, additional-replicator-databases, fair-share]
level: advanced
status: docs-checked
description: "How replication jobs balance and fail over across a CouchDB cluster, add extra /_replicator databases at runtime, and share job slots between them."
sources:
  - https://raw.githubusercontent.com/apache/couchdb/main/src/docs/src/replication/replicator.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Clustering.** Jobs are balanced evenly across nodes, and a job runs on only one node at a time. On every membership change (nodes added or removed, such as a rolling reboot) the replicator rescans documents and running jobs and re-evaluates placement. This also gives fail-over. Jobs from replication documents migrate to a live node; jobs from the `_replicate` HTTP endpoint do not.

**Extra replicator databases** can be added without restart. A `/` in the name must be escaped as `%2F` in URLs:

```
curl -X PUT http://adm:pass@localhost:5984/another%2F_replicator/
```

Add replication documents there, and deleting that database stops its replications; those in `_replicator` continue.

**Fair share.** When a node has more jobs than `max_jobs`, each replicator database gets an equal chance by default (100 shares each). With `max_jobs = 500`: 1000 plus 10 jobs runs about 490 and 10; 200 plus 200 all run; 1000 each runs about 250 each; with 400 shares on `_replicator`, about 400 and 100. Proportions are approximate, and can take tens of minutes to an hour to converge.

## Checked

2026-11-04. Confirmed against the CouchDB replication/replicator page (Replicating in a cluster, Additional Replicator Databases, Fair Share Job Scheduling): even balancing, membership-change rescans and fail-over, _replicate jobs not migrating, runtime addition of a replicator database with %2F escaping, deletion effect, 100 default shares, the four worked examples, convergence time. Nothing removed.

Method: documentation only; no commands were run.
