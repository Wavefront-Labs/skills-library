---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-dual-stack-ipv6
name: k3s-dual-stack-ipv6
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, dual-stack, cluster-cidr, service-cidr, ipv6]
level: advanced
status: docs-checked
description: "Enable IPv4 and IPv6 dual-stack or IPv6-only K3s clusters with cluster-cidr and service-cidr, and avoid known issues."
sources:
  - https://docs.k3s.io/networking/basic-network-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dual-stack must be set when the cluster is first created; it cannot be enabled on a cluster already started as IPv4-only.

Give every server valid dual-stack CIDRs:

```
--cluster-cidr=10.42.0.0/16,2001:db8:42::/56 --service-cidr=10.43.0.0/16,2001:db8:43::/112
```

If you change the cluster-cidr mask, also adjust node-cidr-mask-size-ipv4 and node-cidr-mask-size-ipv6 for pods per node and node count. Largest supported service-cidr mask: /12 for IPv4, /112 for IPv6. Allow IPv6 traffic in public clouds.

Primary family: kubelet uses IPv4 first by default. For IPv6 primary, set node-ip explicitly on all members with the IPv6 address first. Prioritise with `--kubelet-arg="node-ip=0.0.0.0"` (IPv4) or `--kubelet-arg="node-ip=::"` (IPv6).

NAT: for non-routed IPv6 such as ULA ranges, add `--flannel-ipv6-masq`; otherwise pods use their pod IPv6 address outbound. With publicly routed IPv6, route those addresses to the cluster, or pods cannot receive replies; any cluster node forwards pod traffic correctly.

Single-stack IPv6: `--cluster-cidr=2001:db8:42::/56 --service-cidr=2001:db8:43::/112`. If the IPv6 default route comes from a router advertisement, set sysctl `net.ipv6.conf.all.accept_ra=2` or the node drops the route when it expires (accepting RAs may raise man-in-the-middle risk).

Custom CNIs may need extra dual-stack configuration.

## Checked

2026-11-03: read docs.k3s.io networking/basic-network-options. Confirmed: the example dual-stack CIDRs, the node-cidr-mask-size note, the /12 and /112 service-cidr limits, --flannel-ipv6-masq, the single-stack example and the accept_ra=2 sysctl caveat.

Method: documentation only; no commands were run.
