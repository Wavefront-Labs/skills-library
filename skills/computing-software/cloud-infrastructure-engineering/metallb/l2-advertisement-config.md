---
id: computing-software.cloud-infrastructure-engineering.metallb.l2-advertisement-config
name: l2-advertisement-config
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, l2advertisement, layer2, ipaddresspool, arp, ndp, ipaddresspoolselectors]
level: practitioner
status: docs-checked
description: "Configure MetalLB layer 2 mode with an IPAddressPool plus an L2Advertisement, including pool selection and why no IP binding on the node is needed."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/faq/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# L2Advertisement

L2 mode is the simplest: often only IPs are needed. IPs do not need to be bound to node interfaces; MetalLB answers ARP directly with the node's MAC.

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
  - 192.168.1.240-192.168.1.250
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: example
  namespace: metallb-system
```
- An `L2Advertisement` with no `ipAddressPools` selector applies to all pools.
- To advertise only some pools:
```yaml
spec:
  ipAddressPools:
  - first-pool
```
  (a label selector is the alternative).
- An `L2Advertisement` instance must be created; this is different from the original (ConfigMap) MetalLB configuration.
- FAQ: no host interface to specify by default, MetalLB listens and advertises on all interfaces, and only clients on the right network look for the IP. It works with tagged VLANs too. To restrict, see `computing-software.cloud-infrastructure-engineering.metallb.l2-interface-selection`.

The troubleshooting page checks the result with `arping <loadbalancer ip>` from a host on the same L2 subnet (`computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-l2-arping`).

## Checked
2026-11-04. Confirmed against the MetalLB "Configuration" page (L2 section, pool selection), the FAQ (interfaces, VLANs) and the Troubleshooting page (L2Advertisement requirement, arping).
Method: documentation only; no commands were run.
