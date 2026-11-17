---
id: computing-software.cloud-infrastructure-engineering.metallb.requirements-and-memberlist-port
name: requirements-and-memberlist-port
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, requirements, port-7946, memberlist, firewall, prerequisites]
level: intro
status: docs-checked
description: "MetalLB prerequisites: Kubernetes version, compatible network addon, IPv4 addresses, BGP routers, and TCP/UDP 7946 between nodes for L2 mode memberlist."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Requirements

MetalLB needs:
- Kubernetes 1.13.0 or later, with no existing network load-balancing functionality.
- A cluster network configuration that can coexist with MetalLB (`computing-software.cloud-infrastructure-engineering.metallb.network-addon-compatibility`).
- Some IPv4 addresses to hand out.
- BGP mode: one or more routers capable of speaking BGP.
- L2 mode: traffic on port 7946 (TCP and UDP) allowed between nodes, as required by memberlist. The docs say another port can be configured.

Related: `computing-software.cloud-infrastructure-engineering.metallb.l2-leader-election`.

Also before installing:
- Check cloud compatibility (`computing-software.cloud-infrastructure-engineering.metallb.cloud-compatibility`).
- kube-proxy in IPVS mode needs strict ARP (`computing-software.cloud-infrastructure-engineering.metallb.strict-arp-ipvs`).

Background: without a load balancer implementation, LoadBalancer Services stay pending forever on bare metal; the alternatives (NodePort, externalIPs) have significant production downsides.

## Checked

2026-11-04. Confirmed against the MetalLB home page (Requirements: Kubernetes 1.13.0 or later, network config, IPv4 addresses, BGP routers, port 7946 TCP and UDP for memberlist with other ports configurable; the Why section on pending LoadBalancers and NodePort/externalIPs downsides) and the Installation page (strict ARP for IPVS). Removed the unsupported "why it matters" rationale and the firewall Check line.

Method: documentation only; no commands were run.
