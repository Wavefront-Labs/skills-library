---
id: computing-software.data-engineering.apache-kafka.consume-transform-produce-transactions
name: consume-transform-produce-transactions
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, exactly-once, kafka-transactions, consume-transform-produce, sendoffsetstotransaction, transactional-id, read-committed, eos, kip-447]
level: sme
status: docs-checked
description: "Build an exactly-once Kafka-to-Kafka processor with the plain clients: transactional producer, sendOffsetsToTransaction with group metadata, abort handling and read_committed."
sources:
  - https://kafka.apache.org/40/configuration/producer-configs/
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-664%3A+Provide+tooling+to+detect+and+abort+hanging+transactions
  - https://kafka.apache.org/39/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-447%3A+Producer+scalability+for+exactly+once+semantics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consume-transform-produce with Kafka transactions

**Goal:** read from input topics, write results to output topics, and commit input offsets atomically, so each input record affects outputs exactly once even across crashes. (Kafka Streams with `exactly_once_v2` does this for you; use this when you must use plain clients.)

## Configuration
```properties
# producer
transactional.id=enricher-${INSTANCE}      # stable per instance; KIP-447 (2.5+) no longer needs one per input partition
enable.idempotence=true
acks=all
# consumer
group.id=enricher
enable.auto.commit=false
isolation.level=read_committed             # do not read other producers' aborted data
```

## Loop
```java
producer.initTransactions();                         // fences older producers with the same transactional.id
while (running) {
  ConsumerRecords<String, String> recs = consumer.poll(Duration.ofMillis(500));
  if (recs.isEmpty()) continue;
  producer.beginTransaction();
  try {
    for (var r : recs) producer.send(new ProducerRecord<>("orders.enriched.v1", r.key(), enrich(r.value())));
    producer.sendOffsetsToTransaction(nextOffsets(recs), consumer.groupMetadata());   // offsets inside the txn
    producer.commitTransaction();
  } catch (ProducerFencedException | OutOfOrderSequenceException | AuthorizationException e) {
    producer.close(); throw e;                       // fatal: another instance took over, or config issue
  } catch (KafkaException e) {
    producer.abortTransaction();
    rewindToCommitted(consumer, recs.partitions()); // seek back to last committed offsets, then retry
  }
}
```
`nextOffsets` = for each partition, `new OffsetAndMetadata(lastRecordOffset + 1)`. Passing `consumer.groupMetadata()` (not just the group id) lets the coordinator fence zombies by generation (KIP-447).

## Boundaries of the guarantee
- Exactly-once covers **Kafka reads + Kafka writes + offset commits**. Side effects in `enrich()` (HTTP calls, DB writes) are not rolled back on abort: make them idempotent or move them to a sink connector downstream.
- Downstream consumers must use `read_committed`, otherwise they see aborted records.
- `transaction.timeout.ms` (default 60 s) must exceed the time to process one poll batch; the broker rejects larger values via `transaction.max.timeout.ms` (default 15 minutes).
- Transactions add latency: consumers see data only after commit. Commit every poll batch (or every N ms), not per record.

## Monitoring
- `kafka-transactions.sh --bootstrap-server $B list` / `describe --transactional-id X` / `find-hanging` (KIP-664) to find hanging transactions; `abort` subcommand for stuck ones (see hanging-transactions).
- Consumer lag under read_committed is measured to the LSO (last stable offset): a hanging transaction freezes all read_committed consumers on that partition.

## Verify
- [ ] Kill the processor mid-batch repeatedly in a test: output topic has exactly one result per input (check by key/id).
- [ ] Starting a second instance with the same `transactional.id` fences the first (`ProducerFencedException` in its logs).
- [ ] `kafka-transactions.sh list` shows no long-open transactions in steady state.

## Checked
2026-10-28. Confirmed in the KafkaProducer javadoc (3.9), KIP-447, KIP-664, TransactionsCommand source (3.9) and the producer/broker config tables: transactional loop shape (`initTransactions`, `beginTransaction`, `sendOffsetsToTransaction(offsets, consumer.groupMetadata())`, `commitTransaction`, `abortTransaction`), fatal exception group (`ProducerFencedException`, `OutOfOrderSequenceException`, `AuthorizationException`), KIP-447 from 2.5 (one producer per instance, zombie fencing by group metadata), `transaction.timeout.ms` 60 s, `transaction.max.timeout.ms` 15 min, `kafka-transactions.sh list/describe/find-hanging/abort`. The `enrich()`, `nextOffsets` and `rewindToCommitted` helpers are the skill's own illustrative code.
Method: documentation only; no commands were run.
