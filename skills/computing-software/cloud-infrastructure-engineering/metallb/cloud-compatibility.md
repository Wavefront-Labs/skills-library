---
id: computing-software.cloud-infrastructure-engineering.metallb.cloud-compatibility
name: cloud-compatibility
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, cloud-compatibility, floating-ip, aws, azure, gcp, hetzner, keepalived-vip, alternatives]
level: practitioner
status: docs-checked
description: "Which cloud platforms support MetalLB, why most do not (BGP, ARP emulation, floating IPs), and the alternatives: native cloud LB or keepalived-vip."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/installation/clouds.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud compatibility

In general MetalLB is not compatible with cloud providers, even ones offering dedicated servers. Unlisted platforms are probably "no".

Per the docs' table:
- No (use the platform's own): AWS (EKS), Azure (AKS), DigitalOcean (DigitalOcean Kubernetes), Google Cloud (GKE).
- Yes: Hetzner (see their Kubernetes tutorial), OVH (with a vRack), OpenShift OCP, OpenStack, Proxmox, VMware, Vultr.
- OpenShift and OpenStack need changes: `computing-software.cloud-infrastructure-engineering.metallb.openshift-and-openstack-prereqs`.

Why most clouds fail:
- BGP support is usually for inbound route advertisement from off-cloud, so MetalLB BGP either fails or does worse than the cloud LB.
- ARP is emulated by the virtual network, so only IPs the platform assigned resolve; this breaks L2 mode.
- Floating/public IPs use proprietary APIs rather than ARP, so MetalLB cannot grab them.

Alternatives:
1. Use the platform's load balancer product (likely more featureful, with provider-maintained integration).
2. keepalived-vip with shell hooks on failover that call your cloud API. It is VRRP-based (equivalent to L2 mode), LoadBalancer Services still will not work, it mostly suits an HTTP(S) ingress, and documentation is thin.

Cloud API support in MetalLB is out of scope because the project has no funding for test resources.

## Checked

2026-11-04. Read the full MetalLB Cloud Compatibility page: the platform table, the three reasons clouds fail, both alternatives and the funding statement all match. Nothing removed.

Method: documentation only; no commands were run.
