---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-peer-node-selectors
name: bgp-peer-node-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, peer-node-selectors, rack-and-spine, nodeselectors, bgppeer, top-of-rack]
level: advanced
status: docs-checked
description: "Limit which nodes peer with a given router using nodeSelectors on BGPPeer, e.g. each node peers only with its top-of-rack router in a rack-and-spine network."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Limiting peers to certain nodes

By default every node connects to every peer. In a rack-and-spine topology you want each machine to peer with its top-of-rack router only.

Use `nodeSelectors` on the `BGPPeer`; semantics are standard Kubernetes label selectors. The docs' contrived example matches machines that either have `rack=frontend` and not `network-speed=slow`, or have hostname `hostA` or `hostB`:

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
  peerPort: 180
  nodeSelectors:
  - matchLabels:
      rack: frontend
    matchExpressions:
    - key: network-speed
      operator: NotIn
      values: [slow]
  - matchExpressions:
    - key: kubernetes.io/hostname
      operator: In
      values: [hostA, hostB]
```
The example sets `peerPort`, the port of the peer.

This is separate from which nodes advertise a pool (`computing-software.cloud-infrastructure-engineering.metallb.bgp-advertisement-scope`): the BGPAdvertisement node selector is orthogonal, and MetalLB still follows the BGPPeer configuration to choose which node peers with which router.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page, "Limiting peers to certain nodes" and the advertisement subset section. Removed an unsupported tcpdump remark and an invented kubectl label step.
Method: documentation only; no commands were run.
