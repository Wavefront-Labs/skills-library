---
id: computing-software.data-engineering.apache-flink.custom-sink-v2-two-phase-commit
name: custom-sink-v2-two-phase-commit
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, two-phase-commit-sink, sink-v2, committer, exactly-once, custom-sink]
level: sme
status: docs-checked
description: "Build an exactly-once Flink sink with the Sink V2 API: SinkWriter, committables, Committer, idempotent commits, recovery of pending transactions, and testing."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/datastream/sinks/
  - https://github.com/apache/flink/blob/release-2.3/flink-core/src/main/java/org/apache/flink/api/connector/sink2/SupportsCommitter.java
  - https://github.com/apache/flink/blob/release-2.3/flink-core/src/main/java/org/apache/flink/api/connector/sink2/Committer.java
  - https://github.com/apache/flink-connector-kafka/blob/main/docs/content/docs/connectors/datastream/kafka.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom sinks with Sink V2 and two-phase commit

`SinkFunction` is deprecated (its interface says it will be removed in future versions) and now lives in a `legacy` package, as does `TwoPhaseCommitSinkFunction`. The Sink API splits the protocol into a writer and a committer.

## Protocol
1. `SinkWriter.write(record, context)` stages data in a **pre-committable** form (temp file, open transaction, staging table rows).
2. On checkpoint barrier, `prepareCommit()` (on `CommittingSinkWriter`, which a sink that implements `SupportsCommitter` returns) closes the staging unit and returns **committables** (file path, transaction id). Flink stores them in the checkpoint.
3. After the checkpoint completes on all tasks, Flink calls `Committer.commit(requests)` to make them visible (rename file, commit transaction).
4. On recovery, committables from the last completed checkpoint are re-committed: **commit must be idempotent** (committing an already committed transaction is a no-op, not an error; `CommitRequest.signalAlreadyCommitted()` reports that case).

```java
public class TxnSink implements Sink<Row>, SupportsCommitter<TxnHandle> {
  @Override public CommittingSinkWriter<Row, TxnHandle> createWriter(WriterInitContext ctx) {
    String name = "flink-" + ctx.getTaskInfo().getIndexOfThisSubtask() + "-" + ctx.getTaskInfo().getAttemptNumber();
    return new CommittingSinkWriter<>() {
      TxnHandle txn = Store.begin(name);
      public void write(Row r, Context c) { txn.stage(r); }
      public Collection<TxnHandle> prepareCommit() { txn.prepare(); var done = List.of(txn); txn = Store.begin(name); return done; }
      public void flush(boolean endOfInput) {}
      public void close() { /* abort the open, unprepared txn */ }
    };
  }
  @Override public Committer<TxnHandle> createCommitter(CommitterInitContext ctx) {
    return new Committer<>() {
      public void commit(Collection<CommitRequest<TxnHandle>> reqs) {
        for (var r : reqs) {
          try { Store.commitIfNotCommitted(r.getCommittable().id()); }
          catch (RetriableException e) { r.retryLater(); }
          catch (Exception e) { r.signalFailedWithKnownReason(e); }
        }
      }
      public void close() {}
    };
  }
  @Override public SimpleVersionedSerializer<TxnHandle> getCommittableSerializer() { return new TxnHandleSerializer(); }
}
```

## Design rules
- The external system needs a way to keep data invisible but durable until commit (transactions surviving client disconnect, staging files, prepared transactions). If it has none, use an idempotent upsert sink (at-least-once + deterministic keys) instead.
- Transaction timeouts on the external system must exceed the maximum checkpoint duration plus the maximum restart duration, or pending transactions are aborted before commit (for Kafka, the producer `transaction.timeout.ms`).
- Lingering transactions from crashed attempts: derive transactional ids deterministically (subtask + checkpoint id) so a restarted writer can find and abort them.
- Committables serializer is versioned: changing it requires handling old versions for restores.
- Optional topology hooks (`SupportsPreWriteTopology`, `SupportsPostCommitTopology`) add operators before the writer or after the committer, for example merging small files after commit; `SupportsWriterState` adds writer state.

## Testing
- Use `MiniCluster` with checkpointing and a failing map that throws once mid-stream; assert the external store has each record exactly once.
- Test commit idempotency directly: call commit twice with the same committable.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the Sinks page and the release-2.3 source of `Sink`, `SupportsCommitter`, `CommittingSinkWriter`, `Committer.CommitRequest`, `WriterInitContext`/`InitContext`, `TaskInfo` and the legacy `SinkFunction`. Rewrote the example from the removed `TwoPhaseCommittingSink` naming to `Sink` plus `SupportsCommitter` (`createWriter(WriterInitContext)`, `createCommitter(CommitterInitContext)`); corrected the SinkFunction removal claim. The Kafka transaction timeout rule comes from the Kafka connector page.

Method: documentation only; no commands were run.

## Verify
- [ ] Data appears only after checkpoint completion.
- [ ] Failover tests pass repeatedly with no duplicates or losses.
