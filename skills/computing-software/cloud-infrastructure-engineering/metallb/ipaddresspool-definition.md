---
id: computing-software.cloud-infrastructure-engineering.metallb.ipaddresspool-definition
name: ipaddresspool-definition
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, ipaddresspool, cidr, address-range, ipv6, crd, metallb-system, multiple-pools]
level: intro
status: docs-checked
description: "Define MetalLB IPAddressPool resources with CIDRs, ranges and IPv6, use several pools, and keep CRs in the same namespace as MetalLB (metallb-system)."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/faq/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPAddressPool

MetalLB is idle until configured. Configuration is CRs deployed in the same namespace MetalLB runs in (`metallb-system`; with Helm, use the release namespace). Samples: `configsamples` in the metallb repo; full API docs at metallb.io/apis.

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.10.0/24
  - 192.168.9.1-192.168.9.5
  - fc00:f853:0ccd:e799::/124
```
- Addresses can be CIDR or range, IPv4 or IPv6.
- All pools together form the set MetalLB allocates from.
- Multiple pools can coexist, and a pool may list several ranges. Services can pick a pool by annotation (`computing-software.cloud-infrastructure-engineering.metallb.request-specific-ip-or-pool`).
- A single IP in a pool: use `/32` (for example `42.176.25.64/32`).

A pool alone allocates but does not announce. Add an `L2Advertisement` (`computing-software.cloud-infrastructure-engineering.metallb.l2-advertisement-config`) or a `BGPAdvertisement` (`computing-software.cloud-infrastructure-engineering.metallb.bgp-peer-and-advertisement`).

## Checked

2026-11-04. Confirmed against the MetalLB Configuration page (same-namespace CRs, Helm namespace note, configsamples, IPAddressPool example with CIDR, range and IPv6) and the FAQ (several pools, several ranges per pool) and the Advanced AddressPool page (/32 for a single IP). Removed the generic Verify line.

Method: documentation only; no commands were run.
