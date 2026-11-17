---
id: computing-software.networking-hardware-and-wireless.envoy.original-destination-cluster
name: original-destination-cluster
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, original-dst, original-destination, x-envoy-original-dst-host, iptables-redirect, tproxy, filter-state]
level: practitioner
status: docs-checked
description: "Route to the pre-redirect address with an Envoy original destination cluster, including the x-envoy-original-dst-host header override."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/load_balancing/original_dst.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/service_discovery.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# original destination cluster
The original destination load balancer is special purpose and works only with an original destination cluster (`type: ORIGINAL_DST`, `lb_policy: CLUSTER_PROVIDED`). The upstream host is chosen from the downstream connection metadata: connections open to the address the client targeted before being redirected to Envoy by iptables REDIRECT, TPROXY or Proxy Protocol. New destinations are added on demand and the cluster periodically cleans unused hosts (`cleanup_interval`, default 5000 ms). No other policy can be used with it, and subsets cannot be combined with it because hosts are not known in advance.

```yaml
clusters:
- name: original_dst_cluster
  type: ORIGINAL_DST
  lb_policy: CLUSTER_PROVIDED
  connect_timeout: 6s
```
Two overrides:
- HTTP header `x-envoy-original-dst-host` carries a fully resolved `IP:port`, for example `10.195.16.237:8888`.
- Custom extensions can set the filter state object `envoy.network.transport_socket.original_dst_address` to tunnel to an intermediary proxy instead.

Gotcha: if the original address is not available, no upstream connection is opened, and a hostname in the header is not accepted, only an IP. Unvalidated use of that header lets clients steer traffic anywhere reachable, so strip or restrict it at the edge. Verify with `GET /clusters` to see dynamically added hosts.

## Checked

2026-11-03. Confirmed against: original_dst.rst and service_discovery.rst (ORIGINAL_DST, CLUSTER_PROVIDED, x-envoy-original-dst-host, filter state override). Removed or corrected: nothing.

Method: documentation only; no commands were run.
