---
id: computing-software.messaging-and-integration.nats.deterministic-subject-partitioning
name: deterministic-subject-partitioning
category: computing-software
field: messaging-and-integration
product: nats
tags: [partitioning, partition-function, sharding, parallel-consumers, ordering]
level: practitioner
status: docs-checked
description: "Partition message flow with the partition(n, tokens) subject-mapping function so each key always lands on the same consumer subject."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/subject_mapping.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: split one subject space into N deterministic partitions so parallel subscribers each get a stable subset (preserving per-key order).

The mapping function is `partition(<buckets>, <token positions...>)`. It hashes the listed wildcard tokens (or, with only `partition(<buckets>)`, the whole subject) and yields a number from 0 to buckets-1. The same key always maps to the same partition for a fixed bucket count; the hash distribution is random but tends toward even as more keys are seen.

Example from the docs: orders arrive on `neworders.<customer id>`; the mapping
`neworders.* -> neworders.{{wildcard(1)}}.{{partition(3,1)}}`
yields `neworders.<customer id>.<0|1|2>`. Three subscribers can then each take `neworders.*.0`, `neworders.*.1` and `neworders.*.2` and run in parallel. A composite key works too: `foo.{{wildcard(1)}}.{{wildcard(2)}}.{{partition(5,1,2)}}` hashes tokens 1 and 2 into five partitions.

Why not queue groups or durable consumers? Those distribute messages without determinism, so two sequential messages on one subject may reach different subscribers; partitioning keeps a key on one consumer.

Contrast: `random(n)`, e.g. `neworders.{{random(15)}}.create`, spreads load with no key affinity.

Gotchas: changing the bucket count remaps keys; the mapping applies at the scope where it is defined (account, stream, etc.).

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
