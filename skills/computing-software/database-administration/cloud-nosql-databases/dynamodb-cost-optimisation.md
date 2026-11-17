---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-cost-optimisation
name: dynamodb-cost-optimisation
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-cost-optimisation, dynamodb-limits-cost, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: draft
description: "Reduce the DynamoDB bill without hurting latency."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost optimisation

**Goal:** Reduce the DynamoDB bill without hurting latency.

## Steps
- Use Standard-IA class for cold large tables; on-demand for spiky load, provisioned plus reserved capacity for steady load.
- Shorten attribute names, avoid Scan, project fewer attributes into GSIs and delete unused GSIs.
- Use TTL to expire data; eventually consistent reads cost half.
- Check Cost Explorer by usage type and Contributor Insights for hot spots.

## Gotcha
Replicated writes on global tables and GSI writes multiply the write bill; count them.

## Verify
- [ ] Cost per request drops month over month and no Scan dominates ConsumedCapacity.
