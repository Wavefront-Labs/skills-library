---
id: computing-software.cloud-infrastructure-engineering.metallb.k3s-disable-servicelb
name: k3s-disable-servicelb
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, k3s, klipper, servicelb, disable-servicelb, rancher]
level: intro
status: docs-checked
description: "Run MetalLB on K3s by disabling its built-in ServiceLB (formerly Klipper) load balancer with the server option --disable=servicelb."
sources:
  - https://docs.k3s.io/networking/networking-services#disabling-servicelb
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# K3s: disable Klipper

By default K3s provides a load balancer called ServiceLB (formerly Klipper LoadBalancer). To run a different LB such as MetalLB, disable it on all servers in the cluster:
```
--disable=servicelb
```
When ServiceLB is disabled, LoadBalancer Services (including the packaged Traefik Service) stay pending until another load balancer is installed, but their NodePorts are still allocated on every node. MetalLB then allocates from an `IPAddressPool` (`computing-software.cloud-infrastructure-engineering.metallb.ipaddresspool-definition`).

## Checked

2026-11-04. Confirmed against the K3s Networking Services page (Service Load Balancer, Disabling ServiceLB: `--disable=servicelb` on all servers, needed to run MetalLB, behaviour while disabled). The MetalLB k3s page the skill cited is no longer available, so the source was replaced. Removed the svclb pod check and the "both compete" claim, which the page does not state.

Method: documentation only; no commands were run.
