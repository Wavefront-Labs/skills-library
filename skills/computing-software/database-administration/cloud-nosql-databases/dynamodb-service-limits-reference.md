---
id: computing-software.database-administration.cloud-nosql-databases.dynamodb-service-limits-reference
name: dynamodb-service-limits-reference
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [dynamodb-service-limits-reference, dynamodb-limits-cost, dynamodb, amazon-dynamodb, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Design inside DynamoDB quotas."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.Pagination.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service limits reference

**Goal:** Design inside DynamoDB quotas.

## Steps
- Item 400 KB; Query/Scan page 1 MB; batch write 25 items; batch get 100 items; transaction 100 items.
- Default 2,500 tables per Region; 40,000 RCU and 40,000 WCU per table in provisioned mode (defaults, adjustable).
- 20 GSIs and 5 LSIs per table by default; partition key up to 2048 bytes, sort key up to 1024 bytes.
- Nested attribute depth 32 levels.

## Gotcha
Quotas differ by region and may have been raised; check Service Quotas in the console.

## Verify
- [ ] Service Quotas values are recorded and the design headroom is documented.

## Checked
Checked 2026-11-03 against the Service Quotas, naming rules and Query pagination pages: item size, batch and transaction counts, table and per-table throughput defaults, index counts, key sizes, 1 MB page and 32-level nesting match. Removed the unconfirmed 4 KB expression length figure and the "per account" wording on the table count.
Method: documentation only; no commands were run.
