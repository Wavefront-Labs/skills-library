---
id: computing-software.cloud-infrastructure-engineering.metallb.frr-k8s-configuration-merge
name: frr-k8s-configuration-merge
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, frrconfiguration, toreceive, frr-k8s, incoming-prefixes, merge]
level: sme
status: docs-checked
description: "Combine MetalLB with FRR-K8s FRRConfiguration objects, e.g. receive prefixes from a peer, relying on FRR-K8s config merging and its compatibility rules."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/bgp.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FRR-K8s configuration merge

In FRR-K8s mode MetalLB generates a `FRRConfiguration` for each node running a speaker. These can be merged with your own `FRRConfiguration` objects (or those from other controllers) if the FRR-K8s compatibility guidelines are honoured (see "How multiple configurations are merged together" in the frr-k8s README). This lets other uses share MetalLB's FRR instance and BGP sessions.

Example: have a MetalLB-managed peer also receive prefixes:
```yaml
apiVersion: metallb.io/v1beta2
kind: BGPPeer
metadata:
  name: peer
  namespace: metallb-system
spec:
  myASN: 64512
  peerASN: 64512
  peerAddress: 172.30.0.3
---
apiVersion: frrk8s.metallb.io/v1beta1
kind: FRRConfiguration
metadata:
  name: with-recv
  namespace: metallb-system
spec:
  bgp:
    routers:
    - asn: 64512
      neighbors:
      - address: 172.30.0.3
        asn: 64512
        toReceive:
          allowed:
            mode: all
```
FRR-K8s exposes `frrk8s_bgp_received_prefixes_total` (`computing-software.cloud-infrastructure-engineering.metallb.metrics-reference`). The API reference is in the frr-k8s repo (API-DOCS.md). Backend limits: `computing-software.cloud-infrastructure-engineering.metallb.frr-k8s-mode-and-limits`.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page (Configuring with FRR-K8s) and "MetalLB in BGP mode" (merging, shared instance), plus the Prometheus Metrics table. Removed an unsupported neighbor-matching claim and an invented kubectl check.
Method: documentation only; no commands were run.
