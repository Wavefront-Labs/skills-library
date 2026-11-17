---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-graceful-restart
name: bgp-graceful-restart
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, graceful-restart, enablegracefulrestart, bgppeer, rfc4724, upgrades, bfd]
level: advanced
status: docs-checked
description: "Enable BGP graceful restart per MetalLB BGPPeer with enableGracefulRestart (immutable) to cut disruption during upgrades; interaction with BFD is vendor-specific."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP graceful restart

Graceful Restart (RFC 4724) lets BGP routers keep forwarding along known routes while routing information is restored. It applies when the control plane is independent of the forwarding plane, as in most Kubernetes clusters, and was added to minimise disruption during upgrades.

Enable per neighbor:
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
  enableGracefulRestart: true
```
Gotchas:
- The docs note that the `enableGracefulRestart` field is immutable.
- With BFD: per RFC 5882 section 4.3.2, BFD and GR can work together but it is implementation specific. It is up to the vendor's recommendation and needs to be tested (`computing-software.cloud-infrastructure-engineering.metallb.bfd-profile`).

Related: `computing-software.cloud-infrastructure-engineering.metallb.upgrading-metallb`.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page: the Graceful Restart section (RFC 4724, per-neighbor field, immutable, BFD wording). Removed a claim that the router side must enable GR and the delete-and-recreate advice, plus a generic verify line.
Method: documentation only; no commands were run.
