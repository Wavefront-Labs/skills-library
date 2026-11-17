---
id: computing-software.cloud-infrastructure-engineering.thanos.querier-deduplication
name: querier-deduplication
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query, deduplication, replica-label, ha-prometheus]
level: practitioner
status: docs-checked
description: "Deduplicate Prometheus HA replicas at query time with --query.replica-label and the dedup parameter."
sources: ["https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Querier deduplication

Prometheus replicas cannot be load balanced because each has gaps when it restarts. The Querier pulls from both and merges them, filling gaps transparently.

Pick one or more replica labels cluster-wide and pass them to the querier:

```
thanos query \
  --query.replica-label "replica" \
  --query.replica-label "replicaX" \
  --endpoint "<store-api>:<grpc-port>"
```

Series that differ only in the replica label are merged into one. With sidecars labelled `cluster=1,replica=A`, `cluster=1,replica=B` and `cluster=2,replica=A`, `up{env="2"}` returns two series with deduplication and three without.

**Per-request override.** The API accepts `replicaLabels` (overrides the flag) and `dedup` (boolean, default true, but only effective if replica labels are configured). Sending `dedup=false` returns every replica separately.

**Algorithms.** `--deduplication.func` selects:
- `penalty` (default): fills gaps only after a penalty window to avoid flapping between replicas.
- `chain`: 1:1 merge of all samples with no penalty, useful for receiver-based deployments where replicas hold the same data. HA group deduplication is not supported by `chain`.

## Checked

2026-11-03. Confirmed against the Thanos Query page (components/query.md): API parameters and defaults, deduplication algorithms (penalty default, chain), partial response strategies (abort default), endpoint flags and per-endpoint TLS, PromQL engine and distributed mode, tenancy flags, sub-path prefixing. Fixed: --store.sd-files is marked deprecated; per-endpoint TLS does not apply to DNS or static endpoints; partial-response default wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
