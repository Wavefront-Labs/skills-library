---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-power-cooling-and-spares
name: sw-power-cooling-and-spares
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [network-power-redundancy, airflow-direction, hardware-spares-rma]
level: practitioner
status: draft
description: "Choose AC/DC redundant PSUs, match front-to-back airflow to hot/cold aisles, and keep spares and RMA process ready."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Power, cooling, spares

- Dual PSUs on separate feeds (A/B power), and test removal of one feed.
- Airflow direction: data-centre switches ship in port-side-intake or port-side-exhaust variants and fans/PSUs must match; wrong direction recirculates hot air.
- Check power draw at maximum config and PoE load against UPS runtime.
- Keep hot spares of common SKUs (PSUs, fans, optics) and an RMA/support contract with response time matched to criticality. Know serial numbers and contract coverage.
- Environmental monitoring on temperature alarms.

## Verify
- [ ] Pull one PSU and confirm traffic is unaffected and an alarm is raised.
