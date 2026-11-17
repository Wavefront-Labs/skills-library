---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-local-asn
name: bgp-local-asn
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, localasn, local-as, bgppeer, frr, multi-tenant, migration]
level: sme
status: docs-checked
description: "Present a different ASN to one BGP peer with localASN on BGPPeer (FRR mode only), the FRR local-as no-prepend replace-as config it generates, and use cases."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local AS override

FRR can show a peer a different ASN without a separate `router bgp` instance (`neighbor <peer> local-as <ASN> no-prepend replace-as`). MetalLB exposes it as the optional `localASN` field on `BGPPeer`. The router instance keeps using `myASN`; the peer sees `localASN`.

Use it in multi-tenant or migration scenarios where peers on the same node must see different ASNs and VRF separation is undesired or unavailable.

```yaml
apiVersion: metallb.io/v1beta2
kind: BGPPeer
metadata:
  name: example
  namespace: metallb-system
spec:
  myASN: 64512
  peerASN: 64520
  peerAddress: 172.30.0.3
  localASN: 65410
```
Generated `frr.conf`:
```
neighbor 172.30.0.3 remote-as 64520
neighbor 172.30.0.3 local-as 65410 no-prepend replace-as
```
The peer at 172.30.0.3 sees MetalLB's ASN as 65410 rather than 64512.

Constraint: the docs state `localASN` is supported in FRR mode only, and native BGP rejects it at validation. The page does not say whether FRR-K8s supports it; test before relying on it (`computing-software.cloud-infrastructure-engineering.metallb.select-bgp-backend`).

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page, Local AS override section: field name, FRR-only note, generated frr.conf lines, use cases. Removed a verify line that misdescribed which ASN the peer sees.
Method: documentation only; no commands were run.
