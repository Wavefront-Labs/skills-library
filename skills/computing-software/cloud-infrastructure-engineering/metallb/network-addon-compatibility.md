---
id: computing-software.cloud-infrastructure-engineering.metallb.network-addon-compatibility
name: network-addon-compatibility
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, network-addon, cni, kube-router, calico, cilium, flannel, antrea, canal, kube-ovn]
level: practitioner
status: docs-checked
description: "Which CNI network addons are tested with MetalLB (Antrea, Calico, Canal, Cilium, Flannel, Kube-ovn, Kube-router) and the kube-router external BGP peering conflict."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/network-addons.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/kube-router.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network addon compatibility

MetalLB does not care which addon you run as long as it gives the standard behaviours Kubernetes expects. Once traffic lands on a node, the CNI handles the rest.

Tested list (alphabetical, no preference):
- Antrea: yes (tested on 1.4 and 1.5)
- Calico: mostly, see `computing-software.cloud-infrastructure-engineering.metallb.calico-coexistence`
- Canal: yes
- Cilium: yes
- Flannel: yes
- Kube-ovn: yes
- Kube-router: mostly

Untested addons probably work; the docs invite patches.

kube-router: works out of the box with one exception. If you use kube-router's builtin external BGP peering mode, you cannot use MetalLB's BGP mode as well, and there are no plans to address that. kube-router enables strict ARP by default (`computing-software.cloud-infrastructure-engineering.metallb.strict-arp-ipvs`).

## Checked

2026-11-04. Confirmed against the MetalLB Network Addon Compatibility page (addon table, Antrea 1.4 and 1.5), the "Issues with kube-router" page (BGP peering exception, no plans to address) and the Installation page (kube-router enables strict ARP by default). Removed the L2 inference and the generic Check line.

Method: documentation only; no commands were run.
