---
id: computing-software.cloud-infrastructure-engineering.aws.dynamodb-access-pattern-inventory-and-entity-chart
name: dynamodb-access-pattern-inventory-and-entity-chart
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, dynamodb, entity-chart, access-patterns, single-table-design, data-modeling]
level: advanced
status: docs-checked
description: "Start DynamoDB designs with an access pattern inventory and entity chart that map every query to a key condition and index before writing any items."
sources: ["https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ServiceQuotas.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html", "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/contributorinsights_HowItWorks.html", "https://github.com/boto/botocore/blob/develop/botocore/data/dynamodb/2012-08-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access pattern inventory and entity chart

## 1. Access pattern inventory
List every read and write the app will do, with rates, before choosing keys.
| # | Pattern | Type | Rate | Keys used | Index |
|---|---|---|---|---|---|
| 1 | Get customer by id | read | 500/s | PK=`CUST#<id>`, SK=`PROFILE` | table |
| 2 | List orders for customer, newest first | read | 200/s | PK=`CUST#<id>`, SK begins_with `ORDER#`, desc | table |
| 3 | Get order with items | read | 300/s | PK=`ORDER#<id>` | table |
| 4 | Orders by status for ops | read | 5/s | GSI1PK=`STATUS#<s>`, GSI1SK=`<date>` | GSI1 |
| 5 | Place order | write (transaction) | 50/s | Put order + items, update customer counter | table |
Unknown future patterns: note them. A GSI can be added to an existing table (`UpdateTable` accepts GSI
creates), but a local secondary index cannot: `UpdateTable` has no LSI update, so LSIs are defined at table creation.

## 2. Entity chart
| Entity | PK | SK | GSI1PK | GSI1SK |
|---|---|---|---|---|
| Customer | `CUST#<id>` | `PROFILE` | | |
| Order | `CUST#<custId>` | `ORDER#<date>#<id>` | `STATUS#<status>` | `<date>` |
| Order (by id) | `ORDER#<id>` | `META` | | |
| OrderItem | `ORDER#<id>` | `ITEM#<sku>` | | |
Each row is a key template; every pattern in the inventory must be answerable by one `GetItem` or `Query`.
GSI reads are `Query` or `Scan` only (`GetItem` and `BatchGetItem` cannot target an index), and transactions
cannot use indexes, so transactional patterns must be expressed on base-table keys.

## 3. Check the design
- Walk each pattern: which key condition, which index, how many items read, item size.
- Hot keys: the Contributor Insights page states a per-item maximum of 1,000 write request/capacity units
  or 3,000 read units per second; an item or key family expected to exceed that sustained needs sharding.
- Fan-out: patterns needing many queries suggest a missing GSI or denormalised attribute.
- Defaults to plan around: 20 GSIs per table and 5 LSIs per table (the GSI count is a default quota).

## 4. Keep it alive
Store the inventory and chart in the repo next to the table definition; update them with every new feature.

## Verify
- [ ] Every pattern maps to a single Query/GetItem/transaction; no Scans on the request path.

## Checked
Checked 2026-10-24 against the current DynamoDB Developer Guide and the botocore DynamoDB service model.
Confirmed: default 20 GSIs and 5 LSIs per table (Quotas page); `UpdateTable` supports GSI create/update/delete
only and has no LSI member (service model); GSI read operations are `Query` and `Scan` only (GSI page);
transactions cannot be performed using indexes (Transactions page); 1,000 write / 3,000 read units per item
per second ceiling (Contributor Insights page). Removed the NoSQL Workbench step, which was not checked.
Method: documentation only; no commands were run.
