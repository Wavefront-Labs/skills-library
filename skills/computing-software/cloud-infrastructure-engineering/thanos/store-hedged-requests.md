---
id: computing-software.cloud-infrastructure-engineering.thanos.store-hedged-requests
name: store-hedged-requests
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-store, hedged-requests, hedging-config, tail-latency]
level: advanced
status: docs-checked
description: "Tune hedging_config in the Thanos bucket configuration to cut long-tail object storage latency."
sources: ["https://thanos.io/tip/components/store.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Store hedged requests

Hedged requests reduce long-tail latency between the Store Gateway and an external cache or bucket by sending an extra request when the first is slow. Set them under `hedging_config` in the bucket config:

```yaml
hedging_config:
  enabled: false
  up_to: 3
  quantile: 0.9
```

Those are the defaults: with `enabled: true`, up to three additional requests are sent when the first response is slower than the 90th percentile.

- `up_to`: maximum hedged requests per initial request. More lowers latency but can raise cost, since some providers charge per request; returns diminish beyond a point.
- `quantile`: latency threshold that triggers hedging. A lower value such as 0.7 hedges sooner (more cost, less latency variance); a higher value such as 0.95 hedges later (less cost).

## Checked

2026-11-03. Confirmed against the Thanos Store page (components/store.md): disk sizing (6 MB, 30MB), probes, index cache types and config, memcached and redis options, circuit breaker, caching bucket options, groupcache (v0.25, /_groupcache warning), hedging defaults, request limits and deprecations, time partitioning. Removed the claim about raw Prometheus blocks in the data dir. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
