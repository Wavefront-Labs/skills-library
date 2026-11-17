---
id: computing-software.cloud-infrastructure-engineering.thanos.querier-overview
name: querier-overview
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query, querier, global-view, promql]
level: intro
status: docs-checked
description: "What the Thanos Querier does, which StoreAPI backends it can aggregate, and a minimal command line."
sources: ["https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Querier overview

`thanos query` implements the Prometheus HTTP v1 API and evaluates PromQL over data gathered from underlying StoreAPIs. It is stateless and horizontally scalable.

```
thanos query \
  --http-address "0.0.0.0:9090" \
  --endpoint "<store-api>:<grpc-port>" \
  --endpoint "<store-api2>:<grpc-port>"
```

Anything implementing the gRPC StoreAPI is a backend: Prometheus via the Sidecar, object storage via the Store Gateway, the Ruler, the Receiver, another Querier (Queriers can be stacked), and non-Prometheus systems such as OpenTSDB. Queries can mix these sources.

Example global query: `sum(cpu_used{cluster=~"cluster-(eu1|eu2)", job="service1"})`. It works even when each cluster runs several Prometheus servers; the Querier knows which sources to ask.

The API is guaranteed compatible with Prometheus 2.x. Defaults to know: `--query.timeout=2m`, `--query.max-concurrent=20`, `--query.max-concurrent-select=4`, `--query.default-step=1s`.

In the flag list the static `--endpoint` form is marked deprecated in favour of `--endpoint.sd-config`.

## Checked

2026-11-03. Confirmed against the Thanos Query page (components/query.md): API parameters and defaults, deduplication algorithms (penalty default, chain), partial response strategies (abort default), endpoint flags and per-endpoint TLS, PromQL engine and distributed mode, tenancy flags, sub-path prefixing. Fixed: --store.sd-files is marked deprecated; per-endpoint TLS does not apply to DNS or static endpoints; partial-response default wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
