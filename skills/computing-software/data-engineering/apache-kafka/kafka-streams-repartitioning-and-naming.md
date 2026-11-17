---
id: computing-software.data-engineering.apache-kafka.kafka-streams-repartitioning-and-naming
name: kafka-streams-repartitioning-and-naming
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka-streams, repartition-topics, processor-naming, topology-evolution, selectkey, internal-topics]
level: advanced
status: docs-checked
description: "Control Kafka Streams repartition topics: what triggers them, explicit repartition(), naming processors and stores so topology changes don't break state or offsets."
sources:
  - https://kafka.apache.org/documentation/streams/developer-guide/dsl-topology-naming.html
  - https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#repartition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repartition topics and naming processors

## What creates a repartition topic
A key-changing operation (`selectKey`, `map`, `flatMap`, `groupBy` with a new key) followed by a stateful operation (aggregation, join) makes Streams write to `<application.id>-<name>-repartition` and read it back, so records with the same key land on the same task. It costs a full extra write and read through Kafka.
- Prefer `mapValues`/`flatMapValues`/`groupByKey` when the key is unchanged: they do not mark the stream for repartitioning.
- Several downstream stateful ops after one key change: Streams can create multiple repartition topics. Use one explicit `repartition()` and reuse the result.
```java
KStream<String, Order> byCustomer = orders
    .selectKey((k, v) -> v.customerId())
    .repartition(Repartitioned.<String, Order>as("orders-by-customer")
        .withNumberOfPartitions(24)
        .withValueSerde(orderSerde));
```
- `topology.optimization=all` (`StreamsConfig.OPTIMIZE`) merges redundant repartition topics and reuses source topics as changelogs for source KTables. Pass the props to `builder.build(props)` too.

## Why naming matters
Unnamed processors, stores and internal topics get generated names with an index (`KSTREAM-AGGREGATE-STATE-STORE-0000000004`). Adding one operator earlier in the topology shifts the index of everything after it, so after a redeploy:
- state stores and changelogs get new names: state is "lost" (empty store, rebuilt only from new data);
- repartition topics change, so the old topic is no longer read.

Name everything stateful:
```java
orders.groupBy((k, v) -> v.customerId(), Grouped.with("orders-by-customer", Serdes.String(), orderSerde))
      .aggregate(Totals::new, (k, v, agg) -> agg.add(v),
                 Materialized.<String, Totals, KeyValueStore<Bytes, byte[]>>as("customer-totals")
                     .withValueSerde(totalsSerde));
a.join(b, joiner, JoinWindows.ofTimeDifferenceWithNoGrace(Duration.ofMinutes(5)),
       StreamJoined.<String, A, B>as("a-b-join").withStoreName("a-b-join-store"));
```
Set `ensure.explicit.internal.resource.naming=true` (Kafka 4.1+, KIP-1111) to fail at startup if any internal topic or store is auto-named.

## Checks
- Print `topology.describe()` before and after a change; diff the store and topic names.
- Co-partitioned joins need equal partition counts; `repartition(Repartitioned.numberOfPartitions(...))` sets the count.
- The application reset tool (`kafka-streams-application-reset`) deletes the application's internal topics; renamed ones are no longer tracked, so clean up old ones.

## Verify
- [ ] Topology diff shows only intended changes to named stores/topics.
- [ ] After redeploy, state store sizes match pre-deploy.

## Checked
2026-11-01. Confirmed in the Kafka 3.9 Streams docs (DSL topology naming: generated names are numbered by operator position, so inserting an operator shifts state store and changelog names; `Grouped`, `StreamJoined`, `Materialized` naming; `repartition()` and `Repartitioned.numberOfPartitions`; `topology.optimization` values and the `build(Properties)` requirement; app reset tool deletes internal topics; `JoinWindows.ofTimeDifferenceWithNoGrace`) and the 4.1 docs (`ensure.explicit.internal.resource.naming`, KIP-1111). Removed an unconfirmed partition-count default.
Method: documentation only; no commands were run.
