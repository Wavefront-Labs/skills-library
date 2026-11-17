---
id: computing-software.database-administration.neo4j.store-formats-and-checkpoints
name: store-formats-and-checkpoints
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, record-format, block-format, checkpoint-policy, store-format, transaction-logs, checkpoint, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "On-disk layout"
sources:
  - https://neo4j.com/docs/operations-manual/current/database-internals/store-formats/
  - https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Store formats and checkpointing

Goal: understand storage and recovery.
- Store formats are `aligned`, `block`, `high_limit` and `standard`. `block` is the recommended format for Enterprise Edition; `aligned` is the default for Community Edition.
- Checkpointing is configured with `db.checkpoint` settings (policy `PERIODIC` by default, using `db.checkpoint.interval.*`; `VOLUME` is based on transaction log size).
- Transaction log retention is set with `db.tx_log.rotation.retention_policy`.
Verify: restart after a crash recovers without store errors.

## Checked

2026-11-02. Confirmed in the store formats page and configuration settings reference. Removed: the "linked records" description and the claim that logs live in a `transactions/` directory.
Method: documentation only; no commands were run.
