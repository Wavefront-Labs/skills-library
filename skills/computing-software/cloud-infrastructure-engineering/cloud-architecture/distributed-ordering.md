---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.distributed-ordering
name: distributed-ordering
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, distributed-systems-design, distributed-ordering, clocks, lamport-timestamps, vector-clocks, hybrid-logical-clocks, partition-ordering, clock-skew]
level: advanced
status: draft
description: "Handle time and ordering in distributed systems: clock skew, monotonic vs wall clocks, logical and hybrid clocks, per-key ordering in partitions, and conflict resolution."
sources: ["https://lamport.azurewebsites.net/pubs/time-clocks.pdf", "https://cse.buffalo.edu/tech-reports/2014-04.pdf", "https://aws.amazon.com/blogs/compute/implementing-reliable-messaging-with-message-ordering/", "https://kafka.apache.org/documentation/#intro_concepts_and_terms"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clocks and ordering in distributed systems

## Facts
- Wall clocks on different machines disagree (NTP keeps skew to ms, but jumps and leap smearing
  happen). Never order events across machines by wall-clock timestamps alone.
- Use **monotonic clocks** for measuring durations/timeouts within a process.
- Cloud time sync services (Amazon Time Sync, Google/Azure NTP) give tight sync; AWS offers
  microsecond-accuracy PTP on some instances, Google Spanner's TrueTime exposes bounded uncertainty.

## Tools
| Need | Technique |
|---|---|
| Happens-before for causality | Lamport timestamps (total order consistent with causality) |
| Detect concurrent updates | Vector clocks / version vectors |
| Timestamp close to wall time + causality | Hybrid logical clocks (CockroachDB, YugabyteDB) |
| Ordering per entity | Partition by entity key (Kafka partition key, SQS FIFO message group ID, Service Bus sessions) |
| Global total order | Single sequencer / consensus (expensive; limits throughput) |

## Design steps
1. Ask what order actually matters: usually **per key** (per account/order), not global.
2. Route by key to one partition/session; consumers process a partition sequentially.
3. Include a version/sequence number per entity; consumers drop stale updates (`if incoming.version <= stored.version: ignore`).
4. For multi-writer data, choose conflict resolution: last-writer-wins (with HLC), CRDTs, or app merge.

## Gotchas
- LWW with skewed clocks silently drops newer writes.
- Parallel consumers on one partition break ordering.
- Retries reorder messages unless sequence numbers are checked.

## Verify
- [ ] Out-of-order and duplicate delivery test leaves state correct.
