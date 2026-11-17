---
id: computing-software.networking-hardware-and-wireless.envoy.tcp-proxy-network-filter
name: tcp-proxy-network-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, tcp-proxy, l4-proxy, weighted-clusters, metadata-match, envoytcp-proxycluster, idle-timeout]
level: practitioner
status: docs-checked
description: "Proxy raw TCP with the Envoy tcp_proxy network filter, including dynamic cluster selection, weighted clusters and subset routing."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/listeners/network_filters/tcp_proxy_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tcp proxy network filter
The tcp_proxy network filter (`envoy.filters.network.tcp_proxy`) forwards connections to an upstream cluster without parsing the protocol. Outlier detection sees only local (connection) errors from it.

```yaml
filter_chains:
- filters:
  - name: envoy.filters.network.tcp_proxy
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy
      stat_prefix: db
      cluster: postgres
      idle_timeout: 3600s
```
From the docs:
- Dynamic cluster selection: another network filter can set the per-connection filter state object `envoy.tcp_proxy.cluster` to choose the cluster.
- Subset routing: use `TcpProxy.metadata_match` for a single cluster, `ClusterWeight.metadata_match` for weighted clusters, or both (the latter merged on top). Dynamic metadata set on `StreamInfo` by earlier network filters affects load balancing only if set before `onNewConnection()` runs for the TCP proxy.

Gotchas: it does not parse the protocol, so HTTP features such as header routing do not apply. Set `idle_timeout` deliberately; it controls how long an idle connection is kept. Verify with `tcp.<stat_prefix>.*` stats such as downstream_cx_total and `GET /clusters`.

## Checked

2026-11-03. Confirmed against: tcp_proxy_filter.rst and tcp_proxy.proto (cluster, idle_timeout, metadata_match, envoy.tcp_proxy.cluster, stats). Removed or corrected: the sni_cluster advice and the claim that health and retries do not apply.

Method: documentation only; no commands were run.
