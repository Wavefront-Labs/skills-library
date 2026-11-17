---
id: computing-software.data-engineering.streaming-architecture.lambda-vs-kappa-architecture
name: lambda-vs-kappa-architecture
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, lambda-architecture, kappa-architecture, speed-layer, batch-layer, serving-layer, reprocessing, architecture-pattern, dual-pipeline-drift, event-replay]
level: advanced
status: draft
description: "Choose between Lambda (separate batch+speed layers) and Kappa (single streaming pipeline, batch as replay) architectures, and know the real reconciliation cost of Lambda."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - http://nathanmarz.com/blog/how-to-beat-the-cap-theorem.html
  - https://www.oreilly.com/radar/questioning-the-lambda-architecture/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lambda vs Kappa — the cost each one is actually paying for

**Goal:** understand which specific operational cost each architecture avoids and which it accepts, because both are legitimate and the "Kappa is strictly better/newer" narrative skips the real tradeoff.

## 1. Lambda — two pipelines, reconciled
Lambda architecture runs a **speed layer** (streaming, low-latency, often approximate or using a simpler/faster computation) and a **batch layer** (the authoritative, complete recomputation over all data, run periodically) against the same raw data, merging results in a **serving layer** that prefers the batch result once it's available and falls back to the speed layer's fresher-but-less-certain result for the most recent window. This exists because, historically, streaming engines either couldn't guarantee exactly-once/exact correctness at all, or couldn't do so with the same computational model as batch (different APIs, different semantics) — Lambda's batch layer exists specifically as the correctness backstop for a speed layer that might be wrong at the edges.
- **The real cost**: maintaining **two implementations of the same business logic** (once in the streaming engine's API/semantics, once in the batch engine's) that must produce reconcilable results. Logic drift between the two (a bug fixed in the batch job's SQL but not the speed layer's streaming code, or vice versa) is the single most common Lambda failure mode — it doesn't throw an error, it just means the streaming and batch numbers diverge, discovered whenever someone compares them.

## 2. Kappa — one pipeline, reprocessing is replay
Kappa architecture uses a single streaming pipeline for everything; "batch" reprocessing (a bug fix, a backfill) means replaying historical events from the beginning of a durable log (Kafka with long/infinite retention, or a lakehouse table used as a replayable source) through the *same* streaming topology, rather than maintaining a second batch implementation. This was specifically enabled by modern streaming engines (Flink, Kafka Streams) achieving genuine exactly-once/deterministic correctness, removing the historical reason Lambda's batch layer existed as a correctness backstop.
- **The real cost**: replaying a large historical range through a stateful streaming topology at speed (not real-time pace) needs the engine and infrastructure to actually support fast-forwarded replay cleanly — correctly bounding/resetting state, not double-processing against what's already been consumed, and doing so fast enough to be practically useful for a true backfill (replaying a year of data at real-time speed takes a year). This isn't free; it's a different, narrower engineering problem (replay mechanics) traded for avoiding the broader one (two codebases).

## 3. The decision in practice
- Choose **Kappa** when: the streaming engine genuinely supports deterministic, exactly-once semantics for the computation (not every metric type is equally easy to make deterministic under replay), replay/backfill tooling has been built and tested, and the team doesn't want to maintain two codebases for the same logic.
- Choose **Lambda** when: the real-time computation is inherently approximate (a probabilistic/sketch-based speed-layer estimate, e.g. HyperLogLog cardinality, that batch later corrects precisely), when migrating gradually from an existing batch system and a streaming layer is being added incrementally without replacing the batch system outright, or when the organization's existing tooling/expertise makes two simpler, separately-reasoned-about pipelines genuinely easier to build and operate correctly than one more complex replay-capable streaming system.
- Most real systems today lean Kappa-ish for standard pipelines (micro-batch/streaming handling both live and backfill via the same job, per computing-software.data-engineering.etl-pipeline-design.batch-vs-streaming-tradeoffs) and reach for a Lambda-style split only where a genuine real-time-approximation-vs-precision tradeoff exists, not as a default architectural stance.

## 4. The question that actually decides it
"When we need to fix a bug in this pipeline's logic, do we have exactly one place to fix it, and can we re-derive correct historical results from that one fix?" If yes, you have Kappa in practice regardless of what it's called. If the honest answer involves "and then also update the other pipeline to match," you have Lambda, whether or not it was designed that way deliberately — recognize which one you've actually built, since un-deliberate Lambda (two pipelines that evolved independently without anyone deciding to reconcile them) is worse than deliberate Lambda with a planned reconciliation process.

## Verify
- [ ] If running Lambda, a reconciliation check exists that compares speed-layer and batch-layer outputs on an overlap window and alerts on divergence beyond a defined tolerance.
- [ ] If running Kappa, a full historical replay was tested end-to-end (not just theorized) and its runtime for a realistic backfill range is known and acceptable.
- [ ] The choice was made against a named, specific cost (dual-codebase maintenance vs. replay engineering) rather than defaulting to whichever pattern was most recently discussed in a blog post.
- [ ] Any "accidental Lambda" (two independently-evolved pipelines computing related numbers) has been identified and either reconciled deliberately or consolidated.
