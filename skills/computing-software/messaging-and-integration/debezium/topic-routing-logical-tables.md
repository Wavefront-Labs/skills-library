---
id: computing-software.messaging-and-integration.debezium.topic-routing-logical-tables
name: topic-routing-logical-tables
category: computing-software
field: messaging-and-integration
product: debezium
tags: [smt, topic-routing, logical-table, partitioned-tables]
level: practitioner
status: docs-checked
description: "Route events from sharded or partitioned tables into one topic with ToLogicalTopicRouter and keep keys unique."
sources:
  - https://debezium.io/documentation/reference/stable/transformations/topic-routing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default each table has its own topic. The topic routing SMT redirects records before conversion, useful for logical tables (sharded tables with the same schema) and for PostgreSQL partitioned tables, which otherwise go to one topic per partition.

```
transforms=Reroute
transforms.Reroute.type=io.debezium.transforms.ToLogicalTopicRouter
transforms.Reroute.topic.regex=(.*)customers_shard(.*)
transforms.Reroute.topic.replacement=$1customers_all_shards
```

`topic.regex` selects which topics to reroute; `topic.replacement` defines the destination using captured groups. Debezium does not validate the resulting behaviour, so test it. `schema.name.adjustment.mode` is `none` (default) or `avro`.

Unique keys: keys come from primary key columns, which may collide across tables. The SMT inserts a field into the key, named `__dbz__sourceIdentifier` by default. Customise it:

```
transforms.Reroute.key.field.name=shard_id
transforms.Reroute.key.field.regex=(.*)customers_shard(.*)
transforms.Reroute.key.field.replacement=$2
```

With topics `myserver.mydb.customers_shard1..3` the field takes values 1, 2 or 3. If keys are already globally unique, set `key.enforce.uniqueness=false`.

Apply selectively: heartbeat, schema change and transaction messages have a different structure. Use an SMT predicate, or rely on `topic.regex` to match only data topics. A predicate also lets you exclude one table that matches the expression.

Gotcha: never reuse the name of an existing key column in `key.field.name`.

## Checked

2026-11-08. Confirmed against the Debezium page transformations/topic-routing, read in full: ToLogicalTopicRouter options, the default __dbz__sourceIdentifier key field, key.field.regex and replacement, key.enforce.uniqueness, schema.name.adjustment.mode and selective application. Nothing removed.

Method: documentation only; no commands were run.
