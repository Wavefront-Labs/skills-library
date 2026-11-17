---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.target-weight-failover
name: target-weight-failover
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, target, weight, failover, upstreams, admin-api]
level: practitioner
status: docs-checked
description: "Add Targets to a Kong Upstream: target host:port, weight, SRV record overrides, failover backup Targets in v3.12+, and the Admin API call."
sources:
  - https://developer.konghq.com/gateway/entities/target/
  - https://developer.konghq.com/gateway/entities/upstream/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Target weight and failover

A Target is one instance (IP or hostname plus port) of an Upstream.

Fields:
- `target` (required): `host:port`. If the hostname resolves to an SRV record, the DNS port and weight override the configured values.
- `weight`: relative share of traffic for the Target.
- `failover`: when `true` (v3.12+), the Target is used only when all regular Targets are unhealthy.
- `upstream`: parent Upstream by ID or name.

Failover works with the `latency`, `least-connections` and `round-robin` algorithms, not `consistent-hashing` or `sticky-sessions`.

Add one:

```bash
curl -i -X POST http://localhost:8001/upstreams/{upstreamName|Id}/targets/ \
  --header "Content-Type: application/json" \
  --data '{"target": "192.168.1.3:8080", "weight": 50, "failover": true}'
```

decK form:

```yaml
upstreams:
  - name: example_upstream
    targets:
    - target: 192.168.1.3:8080
      weight: 50
      failover: true
```

The `latency` algorithm ignores weights.

## Checked

2026-11-04. Confirmed against the Target and Upstream entity pages: host:port Targets, SRV port and weight override, failover behaviour from 3.12 and supported algorithms, the Admin API and decK examples, latency ignoring weights. Removed the weight default of 100, the 0 to 65535 range and the weight-0 disable rule, and the failover default: the pages' schema tables are empty and the figures appear only in examples.

Method: documentation only; no commands were run.
