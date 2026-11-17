---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.hybrid-roles-listeners
name: hybrid-roles-listeners
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, control-plane, data-plane, cluster-listen, hybrid-mode, role]
level: practitioner
status: docs-checked
description: "Hybrid mode roles and ports in Kong: role=control_plane or data_plane, cluster_listen 8005, cluster_control_plane host:port, telemetry port 8006."
sources:
  - https://developer.konghq.com/gateway/hybrid-mode/
  - https://raw.githubusercontent.com/Kong/kong/master/kong.conf.default
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid roles and listeners

`role` takes `traditional` (default), `control_plane` or `data_plane`.

- **Control plane (CP):** manages configuration, serves the Admin API, and is the only node type connected to the database.
- **Data plane (DP):** serves proxy traffic, runs DB-less, and receives configuration from a CP.

| Parameter | Default | Applies to |
|---|---|---|
| `cluster_listen` | `0.0.0.0:8005` | CP; mTLS protected |
| `cluster_control_plane` | none | DP; `host:port` of the CP |
| `cluster_telemetry_listen` | `0.0.0.0:8006` | CP |
| `cluster_telemetry_endpoint` | none | DP; `host:port` |
| `cluster_telemetry_server_name` | none | SNI for telemetry |

Open ports 8005 and 8006 from data planes to the control plane.

There is no automated load balancing between CP and DP: use multiple CPs behind a TCP proxy.

Read-only Upstream and Target endpoints are exposed on the DP Status API.

Limits: rate limiting plugins (other than `local` and `redis` policies) do not support the `cluster` strategy, OAuth 2.0 authentication is not compatible with hybrid mode, and custom plugins must be installed on both CP and DP.

Certificates and trust: see the cluster_mtls skill.

## Checked

2026-11-04. Confirmed against the Hybrid mode page and kong.conf.default: roles, the listener, endpoint and telemetry settings with defaults, mTLS protection, no automated CP/DP load balancing, Status API endpoints, plugin and custom plugin limits. Nothing removed.
Method: documentation only; no commands were run.
