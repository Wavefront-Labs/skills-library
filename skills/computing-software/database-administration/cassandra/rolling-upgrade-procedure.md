---
id: computing-software.database-administration.cassandra.rolling-upgrade-procedure
name: rolling-upgrade-procedure
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, rolling-upgrade-procedure, news-txt, pre-upgrade-checks, rolling-upgrade, upgradesstables, version-compatibility, nosql, wide-column, cql]
level: practitioner
status: draft
description: "One node at a time"
sources: ["https://cassandra.apache.org/doc/latest/", "https://docs.datastax.com/en/cql/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rolling upgrade procedure

Goal: upgrade without downtime.
- Read NEWS.txt for each version crossed; step through supported paths (for example 4.0 -> 4.1 -> 5.0).
- Per node: `nodetool drain`, stop, upgrade binaries, merge config, start, wait for UN. No schema changes, bootstrap or repair mid-upgrade.
- Afterwards `nodetool upgradesstables`.
- Snapshot first; know your rollback.
Verify: one schema version on the new release.

*Draft written from knowledge; items marked "confirm" are vendor- or version-specific and not yet checked against current documentation.*
