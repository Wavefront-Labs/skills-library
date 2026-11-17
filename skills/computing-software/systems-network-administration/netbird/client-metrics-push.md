---
id: computing-software.systems-network-administration.netbird.client-metrics-push
name: client-metrics-push
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, client-metrics, share-performance-metrics, nb-metrics-push-enabled, metrics-interval]
level: practitioner
status: docs-checked
description: "Control whether NetBird clients push performance metrics: dashboard toggle, version requirements, NB_METRICS_PUSH_ENABLED override and push interval."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/client-metrics.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Clients collect connection-stage timing (signaling, connection, WireGuard handshake), sync duration and login duration. They always collect locally and include it in debug bundles; the setting only controls pushing to a collection server, which is off by default. Peer identifiers are hashed.

Dashboard: Settings > Metrics > Share performance metrics, for all peers. Owners and Admins only. Connected clients apply within seconds; offline ones at next login; changes appear in the activity log.

Versions: dashboard control needs client 0.74.0+. Older clients ignore it and push only with `NB_METRICS_PUSH_ENABLED=true` (supported from 0.67.0).

Override: `NB_METRICS_PUSH_ENABLED` on the client wins over the dashboard.
- `true`: always push.
- `false`: never push (explicit opt-out).
- unset: dashboard applies.

Frequency: `NB_METRICS_INTERVAL` with a duration such as `30m` or `1h`.

For your own monitoring, a client can instead expose a local Prometheus endpoint; see local-metrics-endpoint.

## Checked

2026-11-04: read the Client Metrics page in full. Confirmed what is collected, the off-by-default push, the dashboard path and roles, propagation, the 0.74.0 and 0.67.0 version notes, the NB_METRICS_PUSH_ENABLED precedence table and NB_METRICS_INTERVAL. Nothing removed.

Method: documentation only; no commands were run.
