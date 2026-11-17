---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-dax-cluster-setup
name: dynamodb-dax-cluster-setup
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-dax-cluster-setup, dynamodb-dax, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Add an in-memory read cache cluster in front of DynamoDB for microsecond reads."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAX cluster setup

**Goal:** Add an in-memory read cache cluster in front of DynamoDB for microsecond reads.

## Steps
- Create a subnet group and a cluster of up to 11 nodes (one primary plus replicas); use 3 or more across AZs for fault tolerance. A service role grants DAX access to DynamoDB.
- Use the DAX SDK client (cluster endpoint) in place of the DynamoDB client; no other code change for GetItem/Query/Scan/BatchGetItem.
- Set item TTL and query TTL (default 5 minutes each).

## Gotcha
Writes are write-through; strongly consistent and transactional reads bypass the cache, so they get no speedup.

## Verify
- [ ] Repeat eventually consistent reads of the same item return in microseconds from the cluster endpoint.

## Checked
Checked 2026-11-03 against the DAX concepts and cluster pages: subnet group and service role requirement, 3 or more nodes across AZs, up to 11 nodes, 5 minute default TTLs, write-through and uncached strongly consistent reads match. Removed the unconfirmed ItemCacheHits metric name and the node-type and encryption-in-transit advice, and resolved the TTL "(confirm)".
Method: documentation only; no commands were run.
