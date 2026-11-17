---
id: computing-software.devops-ci-cd.spinnaker.clouddriver-sql-persistence
name: clouddriver-sql-persistence
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [clouddriver, sql, mysql, persistence, caching, dualtaskrepository, sqlcache, aurora]
level: advanced
status: docs-checked
description: "Decide whether to move Clouddriver from Redis to a MySQL-compatible database: what it stores, who benefits, sizing guidance, and the DualTaskRepository for online migration."
sources:
  - https://spinnaker.io/docs/setup/productionize/persistence/clouddriver-sql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Clouddriver can use a MySQL-compatible database instead of Redis for all of its persistence: caching the state of cloud resources and their relationships, the cloud-operations task repository, and distributed locking for the caching-agent scheduler. You may mix Redis for one purpose and SQL for another. A `DualTaskRepository` enables online migration of the task repository between Redis and SQL in either direction without affecting running pipelines.

**Why.** Netflix hit scaling limits with Redis: unordered sets used as secondary indexes cost linear time and are hard to shard without hotspots, and the data is highly relational. After moving to Aurora they saw up to 400% faster loading of the clusters view for large applications (hundreds of server groups, thousands of instances), steadier 99th-percentile times, fewer Clouddriver instances, and tolerance of more than 10x traffic that had previously caused Redis outages.

**Who should bother.** The page says small installations (a few thousand instances across all applications) are unlikely to see significant gains. Redis may eventually be dropped, but it remains fine for evaluation and local development.

**Caveats.** Cache providers may need development to take full advantage of `SqlCache`; the first release adds secondary indexing by application mainly for the UI's `/applications/{application}/serverGroups` calls, and only AWS caching agents use it initially.

**Sizing.** Netflix runs dedicated Aurora clusters for Orca and Clouddriver, though that is not required. Make the full dataset fit in the InnoDB buffer cache; when migrating, provision RAM at about 4x the current Redis working set.

## Checked

Method: docs-checked 2026-11-09 against the first 60 lines (through the start of the sql configuration block) of the spinnaker.io Clouddriver SQL page; the rest of the configuration YAML was not read and is not summarised here. Confirmed what SQL stores, DualTaskRepository, the Netflix results, the small-installation advice, the SqlCache caveat and the sizing rule.
