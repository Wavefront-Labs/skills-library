---
id: computing-software.networking-hardware-and-wireless.envoy.service-discovery-cluster-types
name: service-discovery-cluster-types
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, service-discovery, static, strict-dns, logical-dns, original-dst, eds, cluster-type]
level: practitioner
status: docs-checked
description: "Choose between static, strict DNS, logical DNS, original destination, EDS and custom Envoy cluster discovery types and their drain semantics."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/service_discovery.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# service discovery cluster types
How Envoy learns cluster members:
- Static: addresses are written into config (IP/port or unix socket).
- Strict DNS: continuous async resolution; each returned IP is a host, removed IPs drain from connection pools, and zero results means zero hosts. Duplicate IPs for one name are de-duplicated, but if several names resolve to the same IP, health checking is not shared, so active checks can overload a repeated IP.
- Logical DNS: like strict DNS but only the first returned IP is used when a new connection is initiated; one logical pool may hold connections to varied hosts, connections are never drained, even on a zero-host answer. Suited to large services behind rotating DNS.
- Original destination: for iptables REDIRECT, TPROXY or Proxy Protocol; forwards to the address the client originally targeted, with `cleanup_interval` (default 5000 ms) flushing idle hosts.
- EDS: a gRPC or REST-JSON management server returns endpoints; the preferred mechanism.
- Custom: via the cluster's `cluster_type` field.

```yaml
- name: svc
  type: STRICT_DNS
  load_assignment:
    cluster_name: svc
    endpoints: [ { lb_endpoints: [ { endpoint: { address: { socket_address: { address: svc.internal, port_value: 8080 } } } } ] } ]
```
Gotcha: Envoy assumes service discovery is eventually consistent. With active health checking, a host absent from discovery but still passing checks keeps receiving traffic, and a discovered host that fails its check does not. Admin `/clusters` lists discovered hosts per cluster.

## Checked
2026-11-03. Confirmed against service_discovery.rst, including the cleanup_interval default and the discovery/health check matrix. Removed or corrected: the unsupported 'never resolves DNS in the data path' claim.
Method: documentation only; no commands were run.
