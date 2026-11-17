---
id: computing-software.cloud-infrastructure-engineering.etcd.api-guarantees
name: api-guarantees
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [api-guarantees, linearizability, strict-serializability, ordering, atomicity, durability, consistency, watch-guarantees]
level: advanced
status: docs-checked
description: "Consistency guarantees of etcd's API: durability, strict serializability, linearizable reads, and the ordered, unique, reliable, atomic watch properties."
sources:
  - "https://etcd.io/docs/v3.5/learning/api_guarantees/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The guarantees cover three API groups: KV (Range, Put, Delete, Transaction), Watch and Lease (Grant, Revoke, Keep alive). KV and Watch can read previous versions of keys within a continuous history window limited by compaction.

KV APIs: durability and strict serializability.

- Durability: any completed operation is durable, and all accessible data is durable; a read never returns data that is not durable.
- Strict serializability: operations are atomic and occur in a total order consistent with real-time order, with the order implied by revision. For transactions without nested TXNs, operations execute in the order listed, so GET responses inside are stable; with nested TXNs the order is not specified.
- Atomicity: a request either completes entirely or not at all. All events from one operation arrive in one watch response.
- Linearizability: by default reads reflect the latest completed write. This costs a trip through Raft consensus. A request can be set to `serializable` consistency, which may return data stale with respect to quorum but avoids that cost and gives lower latency and higher throughput.

Watch APIs guarantee events are:

- Ordered by revision; for transactions without nested TXNs, in the order of the operations.
- Unique: an event never appears twice on a watch.
- Reliable: no event is dropped from a sequence within the available history window.
- Atomic: event lists hold complete revisions, never splitting one revision's updates.
- Resumable: a broken watch can restart after the last revision received, if that revision is still in the history window.
- Bookmarkable: progress notifications guarantee all events up to a revision have been delivered.

etcd does not ensure linearizability for watches; check watch event revisions to order them against other operations. Watch results arrive with an unbounded delay: about 10ms in a healthy cluster, possibly never in an unhealthy one.

Leases: created by grant, attached by put, revoked by revoke, and expired by wall-clock TTL. The page points to its "why" notes on lock and lease usage for building correct distributed coordination.

Definitions: an operation is complete once it is committed through consensus and stored by the engine; a client that times out or loses its connection cannot be sure of the outcome, and etcd may abort operations during a leader election without sending abort responses. A transaction gets a single increasing revision even if it modifies the store several times; equal revisions mean modified "concurrently".

## Checked

2026-11-08. Read the v3.5 API guarantees page in full. Confirmed: durability, strict serializability, nested-TXN ordering, linearizable default with serializable option, watch guarantees, operation-complete and revision definitions. Removed: sequential consistency claim, ReadIndex detail, --consistency flag and the lease guarantee claims, none stated on the page.

Method: documentation only; no commands were run.
