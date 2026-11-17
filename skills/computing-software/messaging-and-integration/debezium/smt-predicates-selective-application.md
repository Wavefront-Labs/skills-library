---
id: computing-software.messaging-and-integration.debezium.smt-predicates-selective-application
name: smt-predicates-selective-application
category: computing-software
field: messaging-and-integration
product: debezium
tags: [smt, predicates, tombstone, topic-name-matches]
level: practitioner
status: docs-checked
description: "Apply Debezium SMTs only to matching records with Kafka Connect predicates such as TopicNameMatches and RecordIsTombstone."
sources:
  - https://debezium.io/documentation/reference/stable/transformations/applying-transformations-selectively.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Kafka Connect applies an SMT to every record the connector emits, including heartbeats and schema or transaction metadata that may not fit the SMT. On Apache Kafka 2.6 or later, attach a predicate so the SMT runs only on matching records; non-matching records pass through unchanged.

Predicate elements: the `predicates` list, an alias, a `type`, and any type-specific settings. Associate it with the transform via `transforms.<name>.predicate`, and flip it with `transforms.<name>.negate=true`.

Default types:

- `TopicNameMatches`: true when the topic matches a regular expression `pattern`; use it to scope an SMT by source table.
- `HasHeaderKey`: true for records carrying a given header key.
- `RecordIsTombstone`: true for records with a null value, with no config. Pair it with a filter transform to drop tombstones for sinks that cannot handle them.

```
transforms=outbox
transforms.outbox.type=io.debezium.transforms.outbox.EventRouter
transforms.outbox.predicate=isOutboxTable
predicates=isOutboxTable
predicates.isOutboxTable.type=org.apache.kafka.connect.transforms.predicates.TopicNameMatches
predicates.isOutboxTable.pattern=outbox.event.*
```

A delete produces a delete event (`op: d`) and a tombstone with the same key and null value. Kafka log compaction uses the tombstone to remove prior events for the key. The docs advise letting Debezium emit tombstones, because suppressing them stops compaction from removing deleted keys.

Predicates are reusable across several transforms. You can also define custom predicates.

Gotcha: without a predicate (or the SMT's own `topic.regex`), SMTs such as `ContentBasedRouter` can fail on heartbeat, tombstone and metadata messages, which have a different structure.

## Checked

2026-11-08. Confirmed against the Debezium page transformations/applying-transformations-selectively, read in full: Kafka 2.6 requirement, predicates, type and negate settings, the three default predicate types, the tombstone explanation and the outbox example. Changed the example pattern to the page's outbox.event.* and reworded the closing gotcha to what the pages state.

Method: documentation only; no commands were run.
