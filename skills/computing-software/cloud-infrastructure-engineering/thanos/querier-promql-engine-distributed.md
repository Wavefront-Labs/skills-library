---
id: computing-software.cloud-infrastructure-engineering.thanos.querier-promql-engine-distributed
name: querier-promql-engine-distributed
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query, promql-engine, distributed-execution, query-mode]
level: sme
status: docs-checked
description: "Enable the experimental Thanos PromQL engine and distributed query mode on the Querier."
sources: ["https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Thanos PromQL engine and distributed mode

By default the Querier uses the standard Prometheus PromQL engine (`--query.promql-engine=prometheus`). Setting `--query.promql-engine=thanos` switches to an experimental drop-in engine with a query planner and optimizers. It falls back to the Prometheus engine for anything not yet implemented, so all queries should still work. Report engine bugs in the `thanos-io/promql-engine` repository.

**Distributed execution.** With the Thanos engine, `--query.mode=distributed` makes the Querier split each query into independent fragments and delegate them to components that implement the Query API.

This suits several Queriers deployed in different regions or Kubernetes clusters and federated by a central Querier. Constraints from the docs:
- A distributed-mode Querier talks only to Queriers or other components implementing the Query API.
- Endpoints that are only Stores (Store Gateways, Rulers) attached directly to it are not included in distributed execution.

## Checked

2026-11-03. Confirmed against the Thanos Query page (components/query.md): API parameters and defaults, deduplication algorithms (penalty default, chain), partial response strategies (abort default), endpoint flags and per-endpoint TLS, PromQL engine and distributed mode, tenancy flags, sub-path prefixing. Fixed: --store.sd-files is marked deprecated; per-endpoint TLS does not apply to DNS or static endpoints; partial-response default wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
