---
id: computing-software.database-administration.cockroachdb.multi-active-availability
name: multi-active-availability
category: computing-software
field: database-administration
product: cockroachdb
tags: [multi-active-availability, high-availability, consensus-replication, cap-theorem, quorum]
level: practitioner
status: docs-checked
description: "Explain CockroachDB multi-active availability: every node serves reads and writes, consensus replication keeps data consistent, and quorum loss halts affected data."
sources:
  - https://www.cockroachlabs.com/docs/stable/multi-active-availability
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reason correctly about what a CockroachDB cluster does when nodes fail, and explain it to stakeholders.

Models compared in the docs:
- Active-passive: one active replica, a passive copy. Asynchronous copy can lose data; synchronous copy forces you to trade availability or risk inconsistency when the passive side fails.
- Active-active: all replicas take traffic, but concurrent writes to the same key can diverge after a failure and rejoin (the docs' key `xyz` example). In CAP terms this is an AP system.
- Multi-active availability (CockroachDB): every replica can serve reads and writes, and consensus replication keeps them consistent. Replication requests go to at least 3 replicas, and a change commits once a majority confirms. In CAP terms this is a CP system.

Operational consequences:
- With 3 replicas of a range, one node can fail and the range keeps working; the restarted node catches up with changes it missed.
- If a range loses a majority of its replicas, that data stops responding because consensus is impossible. It resumes when a majority is restored. Consistency is chosen over availability.

Use the architecture overview and the resilience demo pages linked from the doc for deeper detail.

Check your understanding against the page's 3-node example: a write commits once another replica confirms, and if nodes B and C both failed the cluster would stop responding.

## Checked
2026-11-03. Confirmed on the multi-active availability page: active-passive and active-active drawbacks, the `xyz` conflict example, AP versus CP, replication requests to at least 3 replicas committed on majority acknowledgement, and loss of a majority stopping responses until a majority is restored. Removed: the per-range quorum claim and the stop-nodes verification.
Method: documentation only; no commands were run.
