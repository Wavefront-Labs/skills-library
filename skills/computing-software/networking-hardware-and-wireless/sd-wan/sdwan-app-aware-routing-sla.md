---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-app-aware-routing-sla
name: sdwan-app-aware-routing-sla
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-app-aware-routing, sdwan-sla-class, path-selection-policy, sdwan-policy]
level: advanced
status: draft
description: "Define SLA classes (loss, latency, jitter) and application-aware routing policies for steady selection and failover."
sources:
  - https://www.cisco.com/
  - https://www.mef.net/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application-aware routing

- Edges probe each tunnel (BFD or vendor probes) to measure loss, latency and jitter. A policy maps application groups to SLA classes and preferred transports.
- Choose thresholds from application needs (voice: low loss and jitter; bulk: tolerant). Overly tight SLAs cause flapping between paths.
- Use hysteresis/dampening so a brief spike does not trigger a path move.
- Identify applications by DPI signatures or SaaS app lists; confirm accuracy for encrypted traffic.
- Keep a default path for unclassified traffic.

## Verify
- [ ] A deliberately degraded path (lab impairment) moves matching traffic and returns when restored, without oscillation.
