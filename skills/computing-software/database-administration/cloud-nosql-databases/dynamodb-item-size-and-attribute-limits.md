---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-item-size-and-attribute-limits
name: dynamodb-item-size-and-attribute-limits
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-item-size-and-attribute-limits, dynamodb-tables, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Keep items within the 400 KB limit and know what counts toward it."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithTables.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Item size and attribute limits

**Goal:** Keep items within the 400 KB limit and know what counts toward it.

## Steps
- Item size = attribute names (UTF-8 bytes) plus values; short attribute names save space.
- Partition key value max 2048 bytes; sort key value max 1024 bytes; nested attributes up to 32 levels.
- Large blobs go to S3 with the object key stored in the item; split big lists into child items sharing the partition key.
- Reads are metered in 4 KB units and writes in 1 KB units, so rounding up makes a 1.1 KB item cost 2 WCU.

## Gotcha
An item that grows through list append or map updates can suddenly hit 400 KB and every update that would exceed it is then rejected.

## Verify
- [ ] Largest production item is well under 400 KB (check ConsumedCapacity and sample sizes); writes of average items round to the intended WCU.

## Checked
Checked 2026-11-03 against the naming rules and capacity unit calculation pages: 400 KB item limit, attribute names counted in item size, key size limits, 32 nesting levels and 1 KB write / 4 KB read units match. Resolved the key size "(confirm)" and removed the unconfirmed ValidationException error name.
Method: documentation only; no commands were run.
