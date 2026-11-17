---
id: computing-software.cloud-infrastructure-engineering.thanos.querier-partial-response
name: querier-partial-response
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query, partial-response, warn-abort, store-response-timeout]
level: practitioner
status: docs-checked
description: "Choose between availability and accuracy with partial_response_strategy and store timeouts."
sources: ["https://thanos.io/tip/components/query.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Querier partial response

If one StoreAPI errors or times out while others succeed, the result may be missing data. The `PartialResponseStrategy` setting controls the trade-off.

Two strategies exist: `warn` and `abort` (default). The `partial_response` query parameter defaults to the `--query.partial-response` flag, whose default is true.

- On the query API, `partial_response=true` means unavailable stores do not fail the query; the response carries a `warnings` field instead (a 200 status).
- A warning does not always mean lost data (for example "no store matched query").

**Timeouts.** Two settings interact:
- `--query.timeout` (default 2m): maximum time the query node spends on a query.
- `--store.response-timeout` (default 0ms): if a store sends no data in this time it is ignored and partial data is returned, when the strategy is not `abort`.

For availability over accuracy, set `--store.response-timeout` tighter than `--query.timeout`. The extra field in responses is `Warnings []error`, listing non-critical errors.

## Checked

2026-11-03. Confirmed against the Thanos Query page (components/query.md): API parameters and defaults, deduplication algorithms (penalty default, chain), partial response strategies (abort default), endpoint flags and per-endpoint TLS, PromQL engine and distributed mode, tenancy flags, sub-path prefixing. Fixed: --store.sd-files is marked deprecated; per-endpoint TLS does not apply to DNS or static endpoints; partial-response default wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
