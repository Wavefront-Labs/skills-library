---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-hub-ha-and-failover-testing
name: sdwan-hub-ha-and-failover-testing
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-high-availability, sdwan-hub-redundancy, failover-testing]
level: advanced
status: draft
description: "Build redundancy: dual edges per important site, redundant hubs, controller clustering and a failover test plan."
sources:
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SD-WAN high availability

- Site: dual edge routers with FHRP/VRRP or active-active routing; dual circuits on different carriers.
- Hub: two hubs per region on separate sites and transports, with equal or ordered preference; test hub failure.
- Controllers/orchestrators: cluster or deploy redundantly across zones; back up regularly and know the restore procedure.
- Failure tests: circuit loss, edge power-off, hub loss, controller loss, certificate expiry simulation.
- Alert on loss of redundancy, not only on total outage.

## Verify
- [ ] Each failure scenario has a recorded recovery time and an owner.
