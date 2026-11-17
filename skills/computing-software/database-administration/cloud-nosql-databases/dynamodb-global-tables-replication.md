---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-global-tables-replication
name: dynamodb-global-tables-replication
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-global-tables-replication, dynamodb-global-tables, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Replicate a table across regions with multi-active writes."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/V2globaltables_HowItWorks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global tables replication

**Goal:** Replicate a table across regions with multi-active writes.

## Steps
- In multi-Region eventual consistency (MREC) mode, replication uses DynamoDB Streams, which is enabled by default and cannot be disabled. Add a replica: aws dynamodb update-table --table-name Orders --replica-updates '[{"Create":{"RegionName":"eu-west-1"}}]'
- Replication delay is usually a few seconds; watch the ReplicationLatency metric. Replicated writes are billed on each replica.
- Provisioned replicas can throttle from replication writes, so give them auto scaling or use on-demand.
- Settings that stay in sync across replicas include capacity mode, write capacity, TTL, GSI definitions and SSE type; deletion protection, PITR, tags and Contributor Insights are not synced and must be set per replica.
- Concurrent writes to the same item resolve last-writer-wins.

## Gotcha
Replication is asynchronous; a read in one region may not see another region's recent write. Strongly consistent reads only return the latest write if it was made in the same Region.

## Verify
- [ ] describe-table shows each replica ACTIVE and the ReplicationLatency metric stays low.

## Checked
Checked 2026-11-03 against the global tables overview and how-it-works pages: Streams on by default for MREC, last-writer-wins, strongly consistent read scope, the synced and unsynced setting lists, replica throttling and the `--replica-updates` Create form match. Fixed "typically under a second" (docs say usually a few seconds) and the claim that Streams with new and old images must be enabled by the user. Resolved the settings "(confirm)" with the docs lists.
Method: documentation only; no commands were run.
