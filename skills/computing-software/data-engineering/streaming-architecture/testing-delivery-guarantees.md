---
id: computing-software.data-engineering.streaming-architecture.testing-delivery-guarantees
name: testing-delivery-guarantees
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, delivery-guarantee-testing, chaos-testing, exactly-once, at-least-once, fault-injection, testcontainers]
level: advanced
status: draft
description: "Prove a streaming pipeline's at-least-once or exactly-once claim: fault injection (kills, network partitions, broker restarts), sequence-numbered inputs and loss/duplicate checks."
sources:
  - https://jepsen.io/analyses
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/testing/#testing-flink-jobs
  - https://java.testcontainers.org/modules/kafka/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing delivery guarantees under failure

Configuration flags (`enable.idempotence`, `exactly_once_v2`, checkpointing) are necessary, not sufficient. Guarantees break at the edges: sinks, offsets commit order, timeouts. Test the claim end to end.

## Harness
1. **Input with identity**: generator produces records with `(producer_id, seq)` strictly increasing per key, and logs what it acknowledged as sent.
2. **Pipeline under test**: real brokers and processing engine (Testcontainers / docker-compose / a staging namespace), same configs as production.
3. **Sink inspection**: read the final sink (topic with `read_committed`, table, index) and compute per key: missing seqs, duplicated seqs, out-of-order seqs.
4. **Fault injector** running during the load.

## Faults to inject
| Fault | How |
|---|---|
| processor crash | `kill -9` TaskManager / Streams instance / Spark executor and driver |
| graceful restart / deploy | rolling restart, savepoint-stop-start |
| broker loss | stop a broker, leader election mid-transaction |
| network partition / latency | `tc netem`, Toxiproxy between app and broker or sink |
| sink unavailability | stop the database / return 5xx from a mock |
| slow commits | checkpoint/commit timeouts via throttled storage |
| clock jumps | `faketime` on producers (event-time logic) |
Repeat many cycles (dozens of faults per run); bugs show up probabilistically.

## Checks
- **At-least-once**: missing = 0. Duplicates allowed; count them to know the dedup load.
- **Exactly-once**: missing = 0 and duplicates = 0 as observed by a correct reader (read_committed for Kafka; for idempotent upsert sinks, final state equals expected state even if writes repeated).
- **Ordering**: per-key seq strictly increasing in the sink if ordering is claimed.
- Aggregates: final values equal a batch recomputation over the same input.

## Example check (sink is a Kafka topic)
```python
from collections import defaultdict
seen = defaultdict(set); dups = 0
for rec in read_all("out-topic", isolation="read_committed"):
    k, s = rec["key"], rec["seq"]
    dups += s in seen[k]; seen[k].add(s)
missing = sum(len(set(range(1, sent[k] + 1)) - seen[k]) for k in sent)
assert missing == 0, missing
assert dups == 0, dups          # only for exactly-once claims
```

## Gotchas found this way
- Offsets committed before the sink write (auto-commit) = loss on crash.
- Kafka transaction timeout shorter than checkpoint duration = aborted data.
- Non-deterministic processing (wall clock, random, external lookups) makes replays produce different output; "exactly-once" then yields different-but-unique results.

## Verify
- [ ] Test suite runs in CI nightly with a fixed number of fault cycles; results trended.
