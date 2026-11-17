---
id: computing-software.database-administration.cassandra.disk-failure-handling
name: disk-failure-handling
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, disk-failure-policy, commit-failure-policy, jbod-failure, data-directories, tablesnap, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Failing disks"
sources: ["https://cassandra.apache.org/doc/latest/", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk failure policy

Goal: define behaviour on disk errors.
- `disk_failure_policy` (die, stop_paranoid, stop, best_effort, ignore; default stop) and `commit_failure_policy` (die, stop, stop_commit, ignore; default stop).
- `stop` keeps JMX up for diagnosis; replace the node afterwards.
- Alert on I/O errors in system.log.
Verify: kill-test on a non-prod node behaves as designed.

## Checked

2026-11-02. Confirmed against Apache Cassandra trunk docs (doc/modules/cassandra/pages) and conf/cassandra.yaml, nodetool sources: disk_failure_policy and commit_failure_policy values and defaults; stop leaves node inspectable via JMX (cassandra.yaml).
Removed: nothing.
Method: documentation only; no commands were run.
