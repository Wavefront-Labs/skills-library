---
id: computing-software.cloud-infrastructure-engineering.thanos.receive-replication-and-quorum
name: receive-replication-and-quorum
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-receive, replication-factor, write-quorum, capnproto]
level: advanced
status: docs-checked
description: "Set the replication factor, understand the write quorum formula and switch replication to Cap'n Proto."
sources: ["https://thanos.io/tip/components/receive.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Receive replication and quorum

`--receive.replication-factor` (default 1) is how many times each write is replicated across the hashring.

**Write quorum**: the number of replicas that must confirm. For RF 2 the quorum is 1 (the docs keep this so a migration from a 2-Prometheus sidecar setup keeps the same guarantees). Otherwise it is `RF/2 + 1` with integer division: RF 3 needs 2, RF 5 needs 3.

Failed quorum yields 503; the 429 response relates to active-series limits. `--receive.retry-after-backoff` (default 5s) and `--receive.retry-after-jitter` (default 0.5) shape the `Retry-After` header on both.

**Protocol.** Replication defaults to Protobuf over gRPC, which is costly to deserialise and causes GC pressure. Enable Cap'n Proto with `--receive.replication-protocol=capnproto`. Peers' Cap'n Proto addresses are inferred from gRPC addresses, or set explicitly with `capnproto_address` per endpoint; the server listens on `--receive.capnproto-address` (default `0.0.0.0:19391`).

`--receive.grpc-compression` defaults to `snappy` (or `none`). `--receive.forward.async-workers=5` sets a fixed number of forwarding workers; watch `thanos_receive_forward_delay_seconds`.

## Checked

2026-11-03. Confirmed against the Thanos Receive page (components/receive.md) and the Thanos troubleshooting page (operating/troubleshooting.md): hashrings and ketama, shuffle sharding, tenancy and decommissioning, quorum formula, Cap'n Proto, limits and gates, defaults, out-of-bound and out-of-order causes. Added the documented fixes and the out-of-order window flag warnings. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
