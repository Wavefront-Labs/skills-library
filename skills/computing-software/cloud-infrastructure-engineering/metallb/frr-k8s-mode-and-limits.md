---
id: computing-software.cloud-infrastructure-engineering.metallb.frr-k8s-mode-and-limits
name: frr-k8s-mode-and-limits
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, frr-k8s, frr, frr-limitations, bgp, bfd, ipv6, native-bgp]
level: practitioner
status: docs-checked
description: "MetalLB BGP backends: FRR-K8s is the default and FRR is deprecated. Features gained over native, and the RouterID, myAsn, multihop and same-host limits."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/bgp.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FRR-K8s mode and limits

FRR-K8s (a Kubernetes wrapper around FRR with its own API) is the default BGP backend. MetalLB generates FRR-K8s configuration instead of configuring FRR directly. A FRR-K8s instance is deployed on the same nodes as the speaker.

Gains over native BGP:
- BFD-backed BGP sessions
- IPv6 for BGP and BFD
- Multi-protocol BGP
- Merging extra FRR-K8s configuration from users or other controllers, sharing the same FRR instance and sessions

Limitations of FRR-based modes (FRR-K8s and FRR) versus native:
- `RouterID` can be overridden but must be the same for all advertisements.
- `myAsn` can be overridden but must be the same for all advertisements.
- If an eBGP peer is several hops away, set the `ebgp-multihop` flag to true.
- You cannot peer within the same host (native allows it).

FRR mode (MetalLB drives FRR directly) is deprecated and will be removed in a future release. It lacks merging of extra FRR configs. Migrate to FRR-K8s.

Choosing: see `computing-software.cloud-infrastructure-engineering.metallb.select-bgp-backend`. Merging: `computing-software.cloud-infrastructure-engineering.metallb.frr-k8s-configuration-merge`.

## Checked
2026-11-04. Confirmed against the MetalLB "MetalLB in BGP mode" page (FRR-K8s section, limitations of FRR-based modes, deprecated FRR mode) and the MetalLB home page (default backend, features absent from native). Removed an unconfirmed "lightweight" label for native from the description.
Method: documentation only; no commands were run.
