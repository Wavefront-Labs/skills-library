---
id: computing-software.database-administration.neo4j.linux-tuning-neo4j
name: linux-tuning-neo4j
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, nofile-limit, swappiness, filesystem-choice, neo4j-hardware, file-descriptors, transparent-huge-pages, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Host settings"
sources:
  - https://neo4j.com/docs/operations-manual/current/performance/linux-file-system-tuning/
  - https://neo4j.com/docs/operations-manual/current/installation/linux/tarball/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux tuning

Goal: prepare hosts.
- File systems: EXT4 and XFS are both supported; XFS can give marginal gains in some workloads but uses more disk space.
- Check the open-files limit with `ulimit -n`; the tarball install page says the default is 1024, so raise it (the Debian package sets `NEO4J_ULIMIT_NOFILE` to 60000 by default).
Verify: `ulimit -n` for the neo4j user shows the raised value.

## Checked

2026-11-02. Confirmed in the Linux file system tuning page (EXT4 and XFS supported), the tarball page (`ulimit -n`, default 1024) and the Debian page (`NEO4J_ULIMIT_NOFILE` 60000). Removed: swappiness, transparent huge pages, NTP and SSD advice (not on the pages read).
Method: documentation only; no commands were run.
