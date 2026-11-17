---
id: computing-software.messaging-and-integration.nats.nats-bench
name: nats-bench
category: computing-software
field: messaging-and-integration
product: nats
tags: [nats-bench, benchmark, throughput, latency, jetstream-bench]
level: practitioner
status: docs-checked
description: "Benchmark NATS with the nats CLI: core pub/sub, N:M clients, request-reply service latency, JetStream pub/consume/get and KV."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/nats-tools/nats_cli/natsbench.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: measure throughput and latency of your own NATS deployment with `nats bench`.

Prepare a server with monitoring and JetStream: `nats-server -m 8222 -js`. Figures in the docs are examples from one laptop and are not targets.

Core NATS:
- Publisher only: `nats bench pub foo --size 16 --msgs 1000000` (no subscriber, so the number is academic).
- Pub/sub: start the subscriber first, `nats bench sub foo --size 16 --msgs 1000000`, then the publisher. The subscriber starts timing at its first message. Try a larger payload with `--size 16kb`.
- 1:N and N:M fan: `nats bench sub foo --clients 4` with `nats bench pub foo`, or `--clients 4` on both sides.
- Request-reply latency: `nats bench service serve foo` (optionally `--size 16 --clients 2`) and `nats bench service request foo --size 16 --clients 50 --no-progress`.

JetStream:
- Publish: `nats bench js pub sync jsfoo --size 16 --create --storage memory`, `nats bench js pub batch jsfoo --size 16 --batch 1000 --purge --storage memory`, `nats bench js pub async jsfoo --create`.
- Consume: `nats bench js ordered`, `nats bench js consume --clients 4 --no-progress`, `nats bench js fetch --acks none --clients 2`, and direct get with `nats bench js get sync` or `get batch`.
- KV: `nats bench kv put`, then `nats bench kv get --clients 16 --randomize 100000 --no-progress`.

Gotchas: the server warns when JetStream uses a temporary storage directory; memory vs file storage and replica count change results hugely. Clean up the streams and buckets the benchmark created when done (the docs end with a cleanup section).

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
