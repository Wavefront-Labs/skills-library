---
id: computing-software.cloud-infrastructure-engineering.metallb.dual-announce-l2-bgp
name: dual-announce-l2-bgp
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, dual-announce, l2advertisement, bgpadvertisement, ipaddresspool, faq]
level: intro
status: docs-checked
description: "Announce the same MetalLB pool over both L2 and BGP by creating an L2Advertisement and a BGPAdvertisement that reference the same IPAddressPool."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/faq/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Announcing via L2 and BGP together

Yes, it is supported: have an `L2Advertisement` and a `BGPAdvertisement` that reference the same `IPAddressPool`. In the simplest form neither has a selector, so both cover all pools:

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.10.0/24
---
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata:
  name: bgp
  namespace: metallb-system
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: l2
  namespace: metallb-system
```
To restrict, set `ipAddressPools: [first-pool]` on each.

A BGP session to the peers is still required (`computing-software.cloud-infrastructure-engineering.metallb.bgp-peer-and-advertisement`).

The FAQ shows `kubectl get servicel2statuses -n metallb-system` and `kubectl get servicebgpstatuses -n metallb-system` for seeing which node advertises a Service (`computing-software.cloud-infrastructure-engineering.metallb.service-status-resources`).

Trade-offs of each mode: `computing-software.cloud-infrastructure-engineering.metallb.choosing-l2-or-bgp`.

## Checked
2026-11-04. Confirmed against the MetalLB FAQ (same service via L2 and BGP, status resources) and the Configuration page (empty selector means all pools). Removed arping and router verify steps that the pages do not contain.
Method: documentation only; no commands were run.
