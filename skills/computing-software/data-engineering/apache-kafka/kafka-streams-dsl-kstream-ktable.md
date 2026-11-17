---
id: computing-software.data-engineering.apache-kafka.kafka-streams-dsl-kstream-ktable
name: kafka-streams-dsl-kstream-ktable
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-streams, kstream-ktable, globalktable, streams-dsl, repartition-topic, selectkey, groupbykey, application-id, topology]
level: advanced
status: docs-checked
description: "Model Kafka Streams apps with the DSL: KStream vs KTable vs GlobalKTable, re-keying and hidden repartition topics, naming processors, application.id and topology description."
sources:
  - https://kafka.apache.org/39/streams/developer-guide/dsl-api/
  - https://kafka.apache.org/39/streams/core-concepts/
  - https://kafka.apache.org/39/streams/developer-guide/config-streams/
  - https://kafka.apache.org/39/streams/developer-guide/dsl-topology-naming/
  - https://kafka.apache.org/39/streams/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka Streams DSL: KStream, KTable, GlobalKTable

**Goal:** choose the right abstraction for each input and avoid accidental repartitioning and unstable internal topic names.

## Abstractions
| Type | Semantics | Typical input |
|---|---|---|
| `KStream` | Every record is an independent event (insert) | Clickstream, orders placed |
| `KTable` | Changelog: latest value per key (upsert; null = delete), partitioned | Compacted entity topics, aggregations |
| `GlobalKTable` | Full copy of the table on every instance; join by any key without co-partitioning | Small reference data (countries, products) |

```java
StreamsBuilder b = new StreamsBuilder();
KStream<String, Order> orders = b.stream("orders.v1", Consumed.with(Serdes.String(), orderSerde));
KTable<String, Customer> customers = b.table("crm.customer.state.v2",
    Consumed.with(Serdes.String(), customerSerde), Materialized.as("customers-store"));
GlobalKTable<String, Product> products = b.globalTable("ref.products.v1");

orders.selectKey((k, o) -> o.customerId(), Named.as("rekey-by-customer"))   // marks for repartition
      .join(customers, OrderWithCustomer::new)
      .to("orders.enriched.v1", Produced.with(Serdes.String(), enrichedSerde));
```

## Repartition topics
Any key-changing op (`selectKey`, `map`, `groupBy` with a new key) followed by a stateful op (join, aggregate) creates an internal repartition topic: an extra write + read through Kafka. Minimise by:
- Keying data correctly at the producer.
- Using `mapValues`/`flatMapValues` (key unchanged) instead of `map` where possible.
- `groupByKey()` instead of `groupBy(...)` when the key is already right.
- Re-keying once and reusing the stream (`repartition(Repartitioned.numberOfPartitions(...))` explicitly).

## Name everything
Unnamed processors get generated names such as `KSTREAM-FILTER-0000000001`, numbered by position in the topology. State store, changelog and repartition topic names are generated from them and are "stateful": names shift when the topology changes, which matters when you update a running application. Give processors meaningful names with `Named.as` and stores with `Materialized.as`, as the naming page describes. Print the topology to review:
```java
System.out.println(topology.describe());
```

## Key configs
```properties
application.id=orders-enricher        # unique in the cluster; it is also the consumer group ID
bootstrap.servers=...
processing.guarantee=exactly_once_v2
num.stream.threads=4                  # default 1; threads beyond the number of tasks sit idle
replication.factor=3                  # changelog and repartition topics (default -1 = broker default)
state.dir=/var/lib/kafka-streams
```
Maximum parallelism is bounded by the number of stream tasks, which is determined by the maximum number of input topic partitions.

## Checked
2026-10-28. Confirmed on the Kafka 3.9 Streams pages: KStream, KTable and GlobalKTable semantics, `repartition(Repartitioned...)`, `Named.as`, `Materialized.as`, generated `KSTREAM-...-000000000N` names and stateful store/topic naming, `Topology#describe()`, `processing.guarantee=exactly_once_v2`, `num.stream.threads` default 1, `replication.factor` default -1, parallelism bounded by tasks from input partitions. Removed: `Joined.as`, `Grouped.as`, `Repartitioned.as` and the repartition topic name pattern, which the fetched pages do not show.
Method: documentation only; no commands were run.

## Verify
- [ ] `topology.describe()` shows only intended repartition topics and all named stores.
- [ ] `kafka-topics.sh --list | grep <application.id>` matches the expected internal topics.
- [ ] Upgrading the app with a new operator does not change the names of existing stores (name them explicitly).
