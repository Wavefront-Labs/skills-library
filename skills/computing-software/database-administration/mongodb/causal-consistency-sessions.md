---
id: computing-software.database-administration.mongodb.causal-consistency-sessions
name: causal-consistency-sessions
category: computing-software
field: database-administration
product: mongodb
tags: [database-administration, mongodb, mongodb-transactions, causal-consistency, client-session, read-your-writes, majority-read-concern, operation-time, cluster-time]
level: practitioner
status: docs-checked
description: "Get read-your-writes and monotonic reads from MongoDB secondaries with causally consistent sessions plus majority read and write concern."
sources:
  - https://www.mongodb.com/docs/manual/core/causal-consistency-read-write-concerns/
  - https://www.mongodb.com/docs/manual/core/read-isolation-consistency-recency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Causal consistency sessions

**Goal:** a user who writes and then reads (possibly from a secondary) always sees their write, and never sees time go backwards.

## Guarantees in a causally consistent session
Read your writes, monotonic reads, monotonic writes, writes follow reads.

## Use it
Start a client session with causal consistency enabled (see your driver's session options and the manual's driver examples), then inside that session: write with write concern `majority`, then read (optionally with read preference `secondary`) with read concern `majority`, then end the session.

MongoDB returns the operation time and cluster time for majority reads and majority writes in the session and the client session tracks both, so later reads in the session are ordered after earlier operations.

## Concerns matter
Guarantees hold under all failure conditions only with **read concern `majority` and write concern `majority`**. With `w:1`/`local`, a rolled-back write after failover breaks them.

Other combinations may satisfy all four guarantees in some situations but not necessarily all (the manual has the full matrix, for example majority read with `w: 1` keeps only monotonic reads and writes follow reads); treat `majority`/`majority` as the requirement.

## Across processes
Operations can be causally consistent across different sessions: drivers and mongosh can advance the cluster time and operation time of one session to match another (the method names are driver-specific, see your driver), e.g. service A hands its session's times to service B.

## Gotchas
- Applications must ensure that only one thread at a time executes operations within a client session.
- A read from a lagging secondary has to wait for it to catch up, which adds latency.
- Unacknowledged writes (`w: 0`) return no operation time or cluster time and imply no causal relationship.

## Verify
In staging, slow one secondary (throttle its disk) and read with `readPreference: secondary`: inside the session the read after a write returns the new document (waiting if needed); the same read outside the session may not.

## Checked

2026-10-25, against the MongoDB manual source (mongodb/docs repository, content/manual/manual, latest commit 2026-10-23). Confirmed: the four guarantees and the read/write concern matrix (only majority read with majority write gives all four; majority read with w:1 keeps monotonic reads and writes follow reads), two-primary partition behaviour, session tracks operation time and cluster time, operation and cluster time can be advanced across sessions, single-thread-per-session rule, no times for w:0 writes. Removed driver-specific code, afterClusterTime and maxTimeMS claims the manual does not state.

Method: documentation only; no commands were run.
