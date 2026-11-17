---
id: computing-software.database-administration.neo4j.kafka-connector-sink-source
name: kafka-connector-sink-source
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, kafka-connect-neo4j, sink-cypher, source-query, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Neo4j Kafka connector: Cypher sink strategy, query and CDC source strategies, batching, exactly-once offsets and DLQ settings"
sources: ["https://neo4j.com/docs/cypher-manual/current/", "https://neo4j.com/docs/operations-manual/current/", "https://github.com/neo4j/docs-kafka-connector/blob/main/modules/ROOT/pages/sink/cypher.adoc", "https://github.com/neo4j/docs-kafka-connector/blob/main/modules/ROOT/pages/sink/error-handling.adoc", "https://github.com/neo4j/docs-kafka-connector/blob/main/modules/ROOT/pages/source/query.adoc", "https://github.com/neo4j/docs-kafka-connector/blob/main/modules/ROOT/pages/source/cdc.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Neo4j Kafka connector

Goal: integrate Neo4j with Kafka through the Neo4j Connector for Kafka (Kafka Connect sink and source).

## Sink (Cypher strategy)
- Map each topic to a statement with `"neo4j.cypher.topic.<YOUR_TOPIC>": "<cypher>"`.
- From connector 5.1.0 the message header, key and value are bound as `__header`, `__key` and `__value`; `event` still works but is only the value.
- The connector runs each batch with a prepended `UNWIND $events AS message ...`, so write the per-message statement only.
- Batch size is `neo4j.batch-size`, default 1000. With APOC Core present the batch runs via `apoc.cypher.doIt`; otherwise the statement is embedded in a subquery.
- Default delivery is at-least-once, so make statements idempotent (`MERGE`). From 5.5.0 set `neo4j.eos-offset-label` for exactly-once: the connector stores an offset node and the label needs a node key on `strategy`, `topic`, `partition` (a uniqueness constraint on Community Edition). The task fails to start without the constraint; `neo4j.eos-offset-auto-constraint=true` lets the connector create it (needs permission).

## Source
- Choose with `neo4j.source-strategy`: `QUERY` or `CDC`.
- QUERY: set `neo4j.query.topic`, `neo4j.query` (uses the `$lastCheck` parameter) and `neo4j.query.streaming-property` (the cursor, must be in the returned columns). Needs a change-tracking property such as a timestamp, or soft deletes; index that property or polling degrades to full scans.
- CDC: preferred strategy, needs no schema changes and captures deletions reliably. Requires Neo4j Change Data Capture enabled (Neo4j and Aura Enterprise 5 and later). Map patterns to topics, for example `neo4j.cdc.topic.my-topic.patterns` = `(:Person),(:Person)-[:KNOWS]-(:Person)`. After a backup restore (or Aura pause/resume) existing change identifiers stop working and the source must be reconfigured from scratch.

## Poison messages and the DLQ (sink)
- `errors.tolerance` is `none` by default (first error fails the task); `all` skips bad messages.
- Set `errors.deadletterqueue.topic.name` to route failures to a DLQ topic; `errors.deadletterqueue.context.headers.enable=true` adds `__connect.errors.*` headers.
- `errors.deadletterqueue.topic.replication.factor` defaults to 3; set 1 on a single-broker cluster.
- `errors.log.enable` and `errors.log.include.messages` (both default false) control logging of failures and message content.

Verify: produce a test message on each topic and confirm the node or relationship appears; send a malformed one and confirm it lands in the DLQ.

## Checked
2026-11-09

Method: read the connector docs-repo pages sink/cypher, sink/error-handling, source/query and source/cdc (raw asciidoc). Removed: the unverified "confirm current connector options" hedge. Added: batching, exactly-once, CDC and DLQ details from the pages. Not checked: converters and schema registry pages.
