---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.upstream-algorithms
name: upstream-algorithms
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, load-balancing, round-robin, consistent-hashing, upstreams, least-connections]
level: practitioner
status: docs-checked
description: "Kong Upstream load-balancing algorithms: round-robin, consistent-hashing, least-connections, latency (peak EWMA) and sticky-sessions, plus DNS-based balancing."
sources:
  - https://developer.konghq.com/gateway/entities/upstream/
  - https://developer.konghq.com/gateway/load-balancing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upstream algorithms

An Upstream is a load-balancing entity: a virtual hostname plus a set of Targets. A Service can point at an Upstream instead of a host.

`algorithm` values:
- `round-robin`: weighted distribution; supports active and passive health checks.
- `consistent-hashing`: hashes a configured client input to pick a backend (see hash_on).
- `least-connections`: tracks in-flight requests; weights set each backend's capacity; the one with most spare capacity wins.
- `latency`: picks the lowest peak EWMA latency; ignores Target weights.
- `sticky-sessions` (v3.11+): a browser cookie keeps a client on the same Target (`sticky_sessions_cookie` and `sticky_sessions_cookie_path` set the cookie name and path).

Create one:

```bash
curl -i -X POST http://localhost:8001/upstreams/ \
  --header "Content-Type: application/json" \
  --data '{"name": "example-upstream", "algorithm": "round-robin"}'
```

A Service whose hostname resolves to several IPs uses DNS-based balancing automatically: round-robin-like, but with no health checking. Use an Upstream with Targets to get health checks.

## Checked

2026-11-04. Confirmed against the Upstream entity page and the load balancing overview: the five algorithms and their behaviour, sticky-sessions from 3.11, latency ignoring weights, DNS-based balancing without health checks. Removed unconfirmed specifics: round-robin as the default algorithm, name being required, the slots default and range, use_srv_name, and the sticky cookie path default.

Method: documentation only; no commands were run.
