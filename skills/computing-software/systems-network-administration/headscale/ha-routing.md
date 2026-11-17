---
id: computing-software.systems-network-administration.headscale.ha-routing
name: ha-routing
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, high-availability, failover, probe-interval, standby]
level: advanced
status: docs-checked
description: "How Headscale high availability subnet routing picks and fails over routers, and the node.routes.ha probe settings and their limits."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/routes.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/config-example.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# High availability routing

Enabled by default when at least two nodes advertise the same prefix.

## Behaviour

- The router connected to Headscale the longest serves the route.
- A reconnecting router becomes standby.
- A router that stays connected reclaims its routes once approved, healthy and unexpired.
- If no router is available, the last serving router keeps the route.

## Probe settings

```yaml
node:
  routes:
    ha:
      probe_interval: 10s
      probe_timeout: 5s
```

- `probe_interval`: how often HA subnet routers are pinged; 0 disables probing. Must be at least 2s when enabled.
- `probe_timeout`: how long to wait for a ping response before marking a node unhealthy; must be at least 1s and less than `probe_interval`.
- Worst-case detection time is `probe_interval` plus `probe_timeout` (15s with the defaults shown). The config example notes that a node which later responds is marked healthy again but does not reclaim the primary role, to avoid flapping.

## Gotchas

- Both routers need the prefix approved (subnet-routers).
- Check route state with `headscale nodes list-routes`.

## Checked

2026-11-04. Confirmed against the Headscale routes reference (High availability) and config-example.yaml (node.routes.ha defaults and limits). Removed an unsourced claim about failover with probing disabled.
Method: documentation only; no commands were run.
