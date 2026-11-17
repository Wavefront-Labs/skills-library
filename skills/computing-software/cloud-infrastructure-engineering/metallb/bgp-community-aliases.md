---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-community-aliases
name: bgp-community-aliases
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, community-alias, community-crd, communities, bgpadvertisement, no-advertise]
level: practitioner
status: docs-checked
description: "Give BGP communities descriptive names with the MetalLB Community CRD and reference the alias in BGPAdvertisement instead of the 16-bit pair format."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/usage/example.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Community aliases

Define names once with a `Community` resource:
```yaml
apiVersion: metallb.io/v1beta1
kind: Community
metadata:
  name: communities
  namespace: metallb-system
spec:
  communities:
  - name: vpn-only
    value: 1234:1
  - name: NO_ADVERTISE
    value: 65535:65282
```
Use the alias in a `BGPAdvertisement` in place of the two-16-bit-number format:
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
  - vpn-only
```
In the docs' full example, routers understand a "VPN only" community, so sandbox pool routes tagged with it propagate only through the VPN tunnel (`computing-software.cloud-infrastructure-engineering.metallb.full-example-prod-sandbox`).

Communities themselves: `computing-software.cloud-infrastructure-engineering.metallb.bgp-aggregation-and-communities`.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page (Community Aliases section) and the "Full example" page (vpn-only community, 1234:1, VPN-only propagation). Removed an invented kubectl verify command.
Method: documentation only; no commands were run.
