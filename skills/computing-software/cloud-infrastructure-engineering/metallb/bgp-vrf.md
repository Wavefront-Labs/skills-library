---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-vrf
name: bgp-vrf
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, vrf, bgppeer, linux-vrf, frr-k8s, bfd, multi-tenant]
level: advanced
status: docs-checked
description: "Establish MetalLB BGP and BFD sessions over interfaces enslaved to a Linux VRF by setting vrf on BGPPeer; host routing to the CNI remains your job."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/prometheus-metrics/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Peering and announcing via a VRF

Set the `vrf` field on the `BGPPeer` to use interfaces whose master is a Linux VRF (kernel docs: networking/vrf):

```yaml
apiVersion: metallb.io/v1beta2
kind: BGPPeer
metadata:
  name: example
  namespace: metallb-system
spec:
  myASN: 64512
  peerASN: 64512
  peerAddress: 172.30.0.3
  peerPort: 179
  vrf: "red"
```
MetalLB establishes BGP and BFD sessions via interfaces having that VRF as master, and announces services through the interface the session was established from.

Note from the docs: MetalLB attracts traffic toward the interface in the VRF, but some setup on the host network is required for the traffic to reach the CNI, and that falls outside MetalLB's responsibilities.

Metrics: with FRR-K8s, a VRF adds a `vrf` label, e.g. `frrk8s_bgp_updates_total{peer="172.23.0.5",vrf="red"}`.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page (VRF section and note) and the Prometheus Metrics page (vrf label example). Removed an invented host-routing example, an `ip link` verify command and an unrelated cross-reference.
Method: documentation only; no commands were run.
