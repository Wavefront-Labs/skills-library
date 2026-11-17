---
id: computing-software.cloud-infrastructure-engineering.thanos.query-frontend-downstream-tuning
name: query-frontend-downstream-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-query-frontend, downstream-tripper, forward-header, keep-alive]
level: practitioner
status: docs-checked
description: "Tune the HTTP client to the downstream Querier and forward headers such as Authorization."
sources: ["https://thanos.io/tip/components/query-frontend.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Query Frontend downstream tuning

Configure the HTTP client used for `--query-frontend.downstream-url` with `--query-frontend.downstream-tripper-config` or `--query-frontend.downstream-tripper-config-file`.

If the downstream is a single host (most likely a load balancer; the flag help also names localhost and 127.0.0.1), raise `max_idle_conns_per_host` to at least 100. The Go HTTP client keeps only two idle connections per host by default, so without this keep-alive is not used and latency is 10 - 20% higher.

```yaml
max_idle_conns_per_host: 100
```

**Forwarding headers.** `--query-frontend.forward-header` lists request headers passed to downstream queriers (default empty). If queriers need basic auth:

```
thanos query-frontend \
  --query-frontend.forward-header "Authorization" \
  --query-frontend.downstream-url="<thanos-querier>:<querier-http-port>"
```

**Sharding flags.** `--query-range.horizontal-shards`, `--query-range.min-split-interval` and `--query-range.max-split-interval` offer dynamic splitting (not allowed together with `--query-range.split-interval`), and `--query-frontend.vertical-shards` distributes shardable PromQL queries.

## Checked

2026-11-03. Confirmed against the Thanos Query Frontend page (components/query-frontend.md): splitting, retries, limits and defaults, cache behaviour and exclusions, downstream tripper advice (max_idle_conns_per_host 100; 10 - 20% latency), forward-header, sharding flags, --cache-compression-type. Fixed: cache backends wording. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
