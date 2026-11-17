---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.traffic-split-canary
name: traffic-split-canary
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, traffic-split, canary, weighted-upstreams, blue-green, plugin]
level: practitioner
status: docs-checked
description: "Do canary and weighted routing in APISIX with traffic-split: rules.match vars, weighted_upstreams with inline or upstream_id targets, and limits of inline upstreams."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/traffic-split.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# traffic-split canary

Attributes:
- `rules.match[].vars`: lua-resty-expr conditions that must match.
- `rules.weighted_upstreams[]`: `upstream_id` (existing object) or inline `upstream`, plus `weight` (default 1).
- Inline upstream keys include `type` (default `roundrobin`; also `chash`, `ewma`, `least_conn`), `nodes`, `timeout`, `pass_host` (default `pass`), `upstream_host`, `tls`, `keepalive_pool`.

A weighted entry with no `upstream` falls back to the route's own upstream.

```json
{
  "traffic-split": {
    "rules": [
      {
        "match": [ { "vars": [ ["http_release", "==", "new_release"] ] } ],
        "weighted_upstreams": [
          { "upstream": { "type": "roundrobin", "scheme": "https", "pass_host": "node", "nodes": { "httpbin.org:443": 1 } }, "weight": 3 },
          { "weight": 2 }
        ]
      }
    ]
  }
}
```

Requests with header `release: new_release` split 3:2 (60% and 40%) between httpbin.org and the route upstream.

Notes:
- Ratios can drift slightly because selection uses round robin.
- Inline upstreams do not support `service_name`, `discovery_type`, `checks`, `retries`, `retry_timeout`, `desc` or `labels`; define an Upstream object and use `upstream_id` for those.

## Checked

2026-11-04: read the traffic-split plugin page; rules.match.vars, weighted_upstreams with upstream_id, upstream and weight (default 1), the upstream type values and default, pass_host default, the unsupported inline fields, the 3:2 header-matched example (60% and 40%, other entry going to the route upstream) and the round-robin accuracy caveat match. Nothing removed.

Method: documentation only; no commands were run.
