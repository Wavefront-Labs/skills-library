---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-cloud-onramp-saas-iaas
name: sdwan-cloud-onramp-saas-iaas
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-cloud-onramp, saas-direct-internet-access, sdwan-multicloud, sdwan-cloud-resilience]
level: advanced
status: draft
description: "Steer SaaS traffic via best local internet exit and extend the overlay into AWS, Azure or GCP with virtual edges."
sources:
  - https://www.cisco.com/
  - https://www.mef.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud on-ramp

- SaaS (e.g. Microsoft 365): local breakout from branches with path probing to pick the best exit; avoid backhauling to a central proxy where policy allows.
- IaaS: deploy virtual SD-WAN edges in cloud VPC/VNet, or use cloud transit gateways with tunnels; plan IP addressing without overlap.
- Multicloud: consistent segmentation across providers; watch egress costs and cloud throughput limits per virtual instance.
- Combine with a cloud security service (SSE) for internet-bound flows.

## Verify
- [ ] Probe data shows the chosen exit has the lowest latency for the SaaS app and application tests pass.
