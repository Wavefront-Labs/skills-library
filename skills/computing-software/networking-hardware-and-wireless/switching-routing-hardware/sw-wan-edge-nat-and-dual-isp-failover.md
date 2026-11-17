---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-wan-edge-nat-and-dual-isp-failover
name: sw-wan-edge-nat-and-dual-isp-failover
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [wan-edge-nat, dual-isp-failover, ip-sla-tracking]
level: practitioner
status: draft
description: "Configure NAT and dual-ISP failover with reachability tracking (IP SLA/ping probes) so default routes switch on real failures."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dual-ISP edge

- Static default routes with different administrative distance (primary lower) do not withdraw on upstream failures unless tied to a reachability probe. Track a probe (IP SLA / real-time performance monitoring, ping to a stable public target) and bind it to the primary route.
- Probe more than one target to avoid false failovers; keep thresholds and frequency sane.
- NAT per interface: source NAT out of whichever link carries the traffic; existing sessions break on failover (expected).
- Inbound services (port forwards, VPN) need DNS or provider-independent addressing to fail over.
- Test by unplugging the primary and by blocking only the probe target.

## Verify
- [ ] Failover and failback both occur within the planned time and VPNs re-establish.
