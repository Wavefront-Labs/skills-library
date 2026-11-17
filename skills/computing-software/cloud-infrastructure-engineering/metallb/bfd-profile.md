---
id: computing-software.cloud-infrastructure-engineering.metallb.bfd-profile
name: bfd-profile
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, bfd, bfdprofile, bgp, frr-k8s, fast-failure-detection, receiveinterval, transmitinterval]
level: practitioner
status: docs-checked
description: "Back MetalLB BGP sessions with BFD for quicker path failure detection: create a BFDProfile and reference it from a BGPPeer; needs an FRR-based mode."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/prometheus-metrics/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BFD for BGP sessions

BFD needs an FRR-based mode (FRR-K8s or FRR); native BGP has no BFD. It gives faster path failure detection than BGP alone.

1. Create a profile:
```yaml
apiVersion: metallb.io/v1beta1
kind: BFDProfile
metadata:
  name: testbfdprofile
  namespace: metallb-system
spec:
  receiveInterval: 380
  transmitInterval: 270
```
2. Reference it from the peer:
```yaml
apiVersion: metallb.io/v1beta2
kind: BGPPeer
metadata:
  name: peersample
  namespace: metallb-system
spec:
  myASN: 64512
  peerASN: 64512
  peerAddress: 172.30.0.3
  bfdProfile: testbfdprofile
```
The interval values above are the docs' example, not recommended defaults.

FRR-K8s BFD metrics: `frrk8s_bfd_session_up` (1 up, 0 down), plus `frrk8s_bfd_session_down_events` and `frrk8s_bfd_session_up_events` (`computing-software.cloud-infrastructure-engineering.metallb.metrics-reference`).

Graceful restart and BFD: whether they work together is implementation specific; test with your vendor (`computing-software.cloud-infrastructure-engineering.metallb.bgp-graceful-restart`).

## Checked
2026-11-04. Confirmed against the MetalLB "Configuration" page (BFD section, both YAML objects, FRR-based modes) and the Prometheus Metrics page (BFD metric names). The native-has-no-BFD statement matches the Installation page ("no BFD, no IPv6 BGP").
Method: documentation only; no commands were run.
