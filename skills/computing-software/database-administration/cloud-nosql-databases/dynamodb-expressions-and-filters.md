---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-expressions-and-filters
name: dynamodb-expressions-and-filters
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-expressions-and-filters, dynamodb-partiql-queries, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: draft
description: "Use projection, condition, update and filter expressions correctly."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Expressions and filters

**Goal:** Use projection, condition, update and filter expressions correctly.

## Steps
- UpdateExpression: SET #n = :v, counter = counter + :one REMOVE tmp ADD tags :set DELETE oldtags :set.
- Use ExpressionAttributeNames (#n) for reserved words and ExpressionAttributeValues (:v) for values.
- FilterExpression applies after the read, so it does not reduce consumed capacity; the 1 MB page limit applies before filtering.
- ProjectionExpression cuts response size, not read cost.

## Gotcha
A Query with Limit=10 and a FilterExpression may return fewer than 10 or zero items and still have a LastEvaluatedKey.

## Verify
- [ ] Consumed capacity is explained by pre-filter read size and every reserved word attribute is aliased.
