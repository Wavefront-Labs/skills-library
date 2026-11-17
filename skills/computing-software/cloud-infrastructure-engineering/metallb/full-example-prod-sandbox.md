---
id: computing-software.cloud-infrastructure-engineering.metallb.full-example-prod-sandbox
name: full-example-prod-sandbox
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, full-example, production, sandbox, communities, bgpadvertisement, address-pool-annotation]
level: practitioner
status: docs-checked
description: "Worked MetalLB BGP example with a small public production pool, a large private sandbox pool, a vpn-only community and per-service IP or pool selection."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/usage/example.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Full example: production and sandbox

Requirements: production needs public IPs hard-coded in DNS and compliance scans, so specific services need specific addresses. Developer sandboxes come and go and use private space routed over a VPN.

1. Pools:
```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata: {name: production, namespace: metallb-system}
spec:
  addresses: [42.176.25.64/30]    # 4 leased public IPs
---
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata: {name: sandbox, namespace: metallb-system}
spec:
  addresses: [192.168.144.0/20]   # free private space
```
2. Advertisements:
```yaml
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata: {name: external, namespace: metallb-system}
spec:
  ipAddressPools: [production]
---
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata: {name: local, namespace: metallb-system}
spec:
  ipAddressPools: [sandbox]
  communities: [vpn-only]
```
3. A `Community` named `communities` maps `vpn-only` to `1234:1`; the datacenter routers propagate that community only through the VPN tunnel (`computing-software.cloud-infrastructure-engineering.metallb.bgp-community-aliases`).
4. Sandbox Helm charts annotate Services with `metallb.io/address-pool: sandbox`; production Services set `spec.loadBalancerIP` to the exact IP.

MetalLB checks the request fits its configuration, then does what it is told. Request syntax: `computing-software.cloud-infrastructure-engineering.metallb.request-specific-ip-or-pool`.

## Checked

2026-11-04. Read the MetalLB "Full example" page: the requirements, both IPAddressPool objects (42.176.25.64/30 and 192.168.144.0/20), both BGPAdvertisement objects, the Community mapping vpn-only to 1234:1, and the annotation and loadBalancerIP usage all match. Nothing removed.

Method: documentation only; no commands were run.
