---
id: computing-software.cloud-infrastructure-engineering.thanos.querier-api-extensions
name: querier-api-extensions
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query, query-api, auto-downsampling, store-match]
level: practitioner
status: docs-checked
description: "Use Thanos-specific query API parameters such as max_source_resolution, storeMatch and replicaLabels."
sources: ["https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Querier API extensions

Beyond the Prometheus 2.x API, Thanos adds parameters and response fields.

| Parameter | Meaning |
|---|---|
| `dedup` | Deduplicate using replica labels (default true) |
| `replicaLabels` | Overrides `--query.replica-label` per request |
| `partial_response` | Boolean; default from `--query.partial-response` |
| `max_source_resolution` | `auto` (choose automatically), `0` (only raw data), `5m` (max 5m downsampling), `1h` (max 1h downsampling); default `step / 5`, or 0 if `--query.auto-downsampling` is false |
| `storeMatch[]` | Select specific stores |

`--query.auto-downsampling` is false by default.

**Store filtering.** `storeMatch[]` uses federate-style matchers and currently supports only `__address__`, the address shown on the `/stores` UI page. Example:

```
http://localhost:10901/api/v1/query?query=up&dedup=true&partial_response=true&storeMatch[]={__address__=~"prometheus-foo.*"}
```

The docs say this is useful when debugging a slow or broken store.

**Concurrency.** The Querier executes selectors of one PromQL statement concurrently; `--query.max-concurrent-select` (default 4) caps per-query concurrent selects, and `--query.max-concurrent` (default 20) caps concurrent queries. The docs say to consider the combined effect of the two when tuning.

## Checked

2026-11-03. Confirmed against the Thanos Query page (components/query.md): API parameters and defaults, deduplication algorithms (penalty default, chain), partial response strategies (abort default), endpoint flags and per-endpoint TLS, PromQL engine and distributed mode, tenancy flags, sub-path prefixing. Fixed: --store.sd-files is marked deprecated; per-endpoint TLS does not apply to DNS or static endpoints; partial-response default wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
