---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-aggregation-and-communities
name: bgp-aggregation-and-communities
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, aggregationlength, communities, localpref, bgpadvertisement, no-advertise, aggregate-route]
level: advanced
status: docs-checked
description: "Tune MetalLB BGP advertisements with aggregationLength, localPref and communities, e.g. advertise a /24 to transit while keeping /32 routes internal."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Aggregation, localpref and communities

Default: one /32 per allocated IP, localpref 0, no communities.

Scenario: leased /24, transit provider rejects routes more specific than /24, but you want per-IP routing internally. Use two advertisements over one pool (`198.51.100.10/24` in the docs):

```yaml
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata:
  name: local
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
  aggregationLength: 32
  localPref: 100
  communities:
  - 65535:65282
---
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata:
  name: external
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
  aggregationLength: 24
```
For a service on 198.51.100.10, peers receive:
- `198.51.100.10/32` with localpref 100 and the `no-advertise` community (65535:65282): usable by the peer but not propagated.
- `198.51.100.0/24` with no custom attributes, which the peer can propagate to transit.

Each service generates the /24, but MetalLB deduplicates to one advertisement per peer.

Notes: `aggregationLength` cannot be combined with `serviceSelectors`. Name communities with `computing-software.cloud-infrastructure-engineering.metallb.bgp-community-aliases`.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page: defaults (one /32, localpref zero, no communities), both advertisements, the two resulting routes, deduplication, and the serviceSelectors exclusion. Removed a generic verify line.
Method: documentation only; no commands were run.
