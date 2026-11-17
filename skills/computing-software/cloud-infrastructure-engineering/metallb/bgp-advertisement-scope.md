---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-advertisement-scope
name: bgp-advertisement-scope
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, advertisement-scope, peers-subset, nodeselectors, bgpadvertisement, peers]
level: advanced
status: docs-checked
description: "Restrict a MetalLB BGPAdvertisement to certain nodes with nodeSelectors, and to certain BGP peers with the peers list, independently of BGPPeer node selectors."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Advertisement scope: nodes and peers

## Subset of nodes
Make only some nodes next hops for a pool's IPs with `nodeSelectors` on the `BGPAdvertisement`:
```yaml
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata:
  name: example
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
  nodeSelectors:
  - matchLabels:
      kubernetes.io/hostname: NodeA
  - matchLabels:
      kubernetes.io/hostname: NodeB
```
IPs from `first-pool` are then reachable only via NodeA and NodeB. This works at pool/service level and is orthogonal to the BGPPeer node selector (`computing-software.cloud-infrastructure-engineering.metallb.bgp-peer-node-selectors`); MetalLB still follows BGPPeer config to decide which nodes peer with which router.

## Subset of peers
By default each service IP goes to all connected peers. Limit with `peers`:
```yaml
spec:
  ipAddressPools:
  - PoolA
  peers:
  - PeerA
  - PeerB
```
IPs from PoolA go only to PeerA and PeerB (the docs' diagram has PoolB going to PeerB and PeerC).

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page: both sections, the YAML and the diagram description. Removed a generic verify line the page does not contain.
Method: documentation only; no commands were run.
