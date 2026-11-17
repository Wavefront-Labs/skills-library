---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-service-selectors
name: bgp-service-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, bgp-serviceselectors, serviceselectors, bgpadvertisement, localpref, aggregationlength]
level: advanced
status: docs-checked
description: "Apply different BGP policies per service with serviceSelectors on BGPAdvertisement, e.g. higher localPref for production; mutually exclusive with aggregationLength."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_bgp_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP service selectors

By default a `BGPAdvertisement` applies to all Services that got an IP from its pools. `serviceSelectors` limits it to Services whose labels match.

```yaml
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata:
  name: production-services
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
  localPref: 200
  serviceSelectors:
  - matchLabels:
      environment: production
---
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata:
  name: staging-services
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
  localPref: 100
  serviceSelectors:
  - matchLabels:
      environment: staging
```
Services labelled `environment: production` from `first-pool` get localPref 200; `staging` ones get 100.

Rules:
- Multiple selectors are ORed: matching any selector is enough.
- `serviceSelectors` is mutually exclusive with `aggregationLength` and `aggregationLengthV6`; it needs the default /32 (IPv4) or /128 (IPv6) because aggregated routes cannot belong to individual services.

The L2 counterpart is `computing-software.cloud-infrastructure-engineering.metallb.l2-service-selectors`.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced BGP configuration" page, "Limiting the advertisement to specific services": both examples, OR logic and the mutual-exclusion note. Removed a generic verify line.
Method: documentation only; no commands were run.
