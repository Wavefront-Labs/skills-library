---
id: computing-software.cloud-infrastructure-engineering.metallb.calico-coexistence
name: calico-coexistence
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, calico, serviceloadbalancerips, bgpconfig, calicoctl, bgp-session-conflict, spine, vrf]
level: advanced
status: docs-checked
description: "Run MetalLB with Calico: let Calico (3.18+) announce LoadBalancer IPs via BGPConfig, or work around the one-BGP-session limit by peering with spines or using router VRFs."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/calico.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calico coexistence

## Easy way (Calico 3.18 and later)
Calico can announce LoadBalancer IPs via BGP. Run MetalLB, apply an `IPAddressPool` with no `BGPAdvertisement`. You can even remove the speaker pods, since the controller assigns IPs.
```bash
calicoctl patch BGPConfig default --patch '{"spec": {"serviceLoadBalancerIPs": [{"cidr": "10.11.0.0/16"},{"cidr":"10.1.5.0/24"}]}}'
```
Calico announces the entire CIDR block given, not individual IPs; list more specific routes explicitly if you need them.

## Hard way (older Calico)
Problem: BGP allows one session per pair of nodes, so if Calico holds the session to your router MetalLB's duplicate is rejected. Calico lacks extension points to fix this.

Workarounds:
- Peer MetalLB with the spine routers instead of the ToRs (Calico keeps the ToR sessions). Cost: extra config, and sessions scale with machine count rather than racks. A compromise is dedicating some racks to external services: constrain the speaker DaemonSet to them, and use `externalTrafficPolicy: Cluster` or constrain service pods to those racks.
- Router VRFs: peer Calico and MetalLB to separate VRFs of one router and leak routes carefully. The docs say this is theoretical and not demonstrated.

## Checked

2026-11-04. Read the full MetalLB "Issues with Calico" page: Calico 3.18, IPAddressPool without BGPAdvertisement, optional removal of speaker pods, the calicoctl BGPConfig example, whole-CIDR announcement, one-session-per-pair problem, spine peering, rack-dedication compromise and the VRF workaround all match. Nothing removed.

Method: documentation only; no commands were run.
