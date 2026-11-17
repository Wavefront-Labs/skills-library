---
id: computing-software.cloud-infrastructure-engineering.metallb.l2-service-selectors
name: l2-service-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, l2-serviceselectors, serviceselectors, l2advertisement, allow-shared-ip, interfaces]
level: advanced
status: docs-checked
description: "Choose L2 announcement settings per service by label with serviceSelectors on L2Advertisement, and why it breaks Services using allow-shared-ip."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_l2_configuration.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/usage/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# L2 service selectors

By default an `L2Advertisement` applies to every Service with an IP from its pools. `serviceSelectors` narrows it by Service labels, e.g. different interfaces per tier:

```yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: frontend-services
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
  interfaces:
  - eth0
  serviceSelectors:
  - matchLabels:
      tier: frontend
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: backend-services
  namespace: metallb-system
spec:
  ipAddressPools:
  - first-pool
  interfaces:
  - eth1
  serviceSelectors:
  - matchLabels:
      tier: backend
```
`tier: frontend` Services from `first-pool` are announced from eth0; `tier: backend` from eth1. Several selectors in the list are ORed.

Warning: `serviceSelectors` is incompatible with the `metallb.io/allow-shared-ip` annotation. Services using `allow-shared-ip` that match an L2Advertisement with `serviceSelectors` are not announced, because Services sharing one IP could match different advertisements and cause split announcements (`computing-software.cloud-infrastructure-engineering.metallb.ip-sharing`).

BGP counterpart: `computing-software.cloud-infrastructure-engineering.metallb.bgp-service-selectors`.

## Checked
2026-11-04. Confirmed against the MetalLB "Advanced L2 configuration" page (serviceSelectors section, examples, OR logic, allow-shared-ip warning) and the Usage page (same warning). Removed a generic verify line.
Method: documentation only; no commands were run.
