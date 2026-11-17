---
id: computing-software.networking-hardware-and-wireless.envoy.management-server-connectivity-and-stats
name: management-server-connectivity-and-stats
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, management-server, control-plane, connected-state, tcp-keepalive, xds-stats, version-text]
level: practitioner
status: docs-checked
description: "Detect and survive an unreachable xDS management server: keepalives on the xDS cluster, the control_plane.connected_state gauge and subscription stats."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/overview/mgmt_server.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/overview/xds_api.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# management server connectivity and stats
When Envoy loses the management server it latches onto the last configuration and retries in the background; running traffic keeps flowing. Because a half-open connection may never error, configure TCP keepalives or HTTP/2 keepalives on the cluster that connects to the management server so Envoy notices and reconnects.

```yaml
clusters:
- name: xds_cluster
  type: STRICT_DNS
  typed_extension_protocol_options:
    envoy.extensions.upstreams.http.v3.HttpProtocolOptions:
      "@type": type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions
      explicit_http_config:
        http2_protocol_options:
          connection_keepalive: { interval: 30s, timeout: 5s }
```
The `control_plane.*` stats tree holds `connected_state` (gauge, 1 connected, 0 disconnected), `rate_limit_enforced`, `pending_requests` and `identifier` (the control plane instance that sent the last response). Alert on `control_plane.connected_state == 0`; Envoy only debug-logs failed reconnects, so the gauge is the signal.

xDS transport endpoints for the v3 gRPC API follow the pattern `/envoy.service.cluster.v3.ClusterDiscoveryService/StreamClusters`, `/envoy.service.endpoint.v3.EndpointDiscoveryService/StreamEndpoints` and so on. Each subscription also has per-resource-type stats (update_success, update_rejected, version).

Gotcha: a rejected update keeps the old config silently from the dataplane's view; watch `update_rejected`. Verify with `GET /stats?filter=control_plane` and `GET /config_dump`.

## Checked

2026-11-03. Confirmed against: mgmt_server.rst (keepalives, debug logging, control_plane stats, subscription stats). Removed or corrected: nothing.

Method: documentation only; no commands were run.
