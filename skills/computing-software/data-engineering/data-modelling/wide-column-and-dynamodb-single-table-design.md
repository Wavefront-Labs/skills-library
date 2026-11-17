---
id: computing-software.data-engineering.data-modelling.wide-column-and-dynamodb-single-table-design
name: wide-column-and-dynamodb-single-table-design
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, wide-column-modelling, dynamodb-single-table, cassandra, key-value]
level: sme
status: draft
description: "Model for key-value and wide-column stores (DynamoDB single-table, Cassandra): access-pattern-first keys, partition/sort key design, GSIs, hot partitions and limits."
sources:
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html
  - https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html
  - https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key-value and wide-column modelling

**Goal:** single-digit-ms queries at any scale by designing keys for the exact access patterns.

## Start from access patterns
List every query with its key inputs and sort needs, e.g.:
1. Get customer by id.
2. List a customer's orders, newest first.
3. Get order with its items.
4. List orders by status for a day (admin).
No ad-hoc queries later without new indexes; this is the trade.

## DynamoDB single-table
| Entity | PK | SK |
|---|---|---|
| Customer | `CUST#123` | `PROFILE` |
| Order | `CUST#123` | `ORDER#2026-10-18#9876` |
| Order item | `ORDER#9876` | `ITEM#001` |
- Pattern 2: `Query PK = CUST#123 AND begins_with(SK, 'ORDER#')`, `ScanIndexForward=false`.
- Pattern 4: GSI with `GSI1PK = STATUS#shipped#2026-10-18`, `GSI1SK = ORDER#...`.
- Item limit 400 KB; 1 MB per Query page.

## Cassandra
One table per query; partition key = what you filter by equality, clustering columns = sort order.
```sql
CREATE TABLE orders_by_customer (
  customer_id uuid, order_ts timestamp, order_id uuid, total decimal,
  PRIMARY KEY ((customer_id), order_ts, order_id)
) WITH CLUSTERING ORDER BY (order_ts DESC);
```
Denormalise: the same order is written to several query tables.

## Hot partitions and size
- High-cardinality partition keys spread load; a status or date alone as partition key concentrates writes.
- Write sharding: append a suffix (`STATUS#shipped#2026-10-18#7`) and query all shards.
- Cassandra: keep partitions under ~100 MB / 100k rows; bucket time series by day/month in the key.

## Analytics
Export via DynamoDB export to S3 / Cassandra CDC into the lake; single-table items need to be split by entity type (SK prefix) in the warehouse.

## Verify
Every access pattern maps to one Query/GetItem (no Scan); CloudWatch/nodetool shows no throttled or oversized partitions under load tests.
