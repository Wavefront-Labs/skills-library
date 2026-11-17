---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-control-management-data-planes
name: sdwan-control-management-data-planes
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-architecture, sdwan-orchestrator-controller, sdwan-control-plane, sdwan-architecture]
level: intro
status: draft
description: "Explain management, control and data planes of SD-WAN, where each runs, and what survives when the controller is unreachable."
sources:
  - https://www.mef.net/
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SD-WAN planes

- Management/orchestration plane: policy and template definition, monitoring (e.g. Cisco SD-WAN Manager, Fortinet FortiManager, Versa Director).
- Control plane: distributes routes, keys and policies between edges (e.g. OMP with controllers in Cisco SD-WAN).
- Data plane: edge devices form IPsec (or vendor) tunnels across transports and forward user traffic.
- Edges generally keep forwarding on cached state if controllers are unreachable, for a limited time or indefinitely depending on vendor; confirm behaviour and graceful-restart timers.
- Cloud-hosted vs on-prem controllers changes upgrade control, compliance, and failure domain.

## Verify
- [ ] A lab test of controller loss shows edge forwarding behaviour matching the design assumptions.
