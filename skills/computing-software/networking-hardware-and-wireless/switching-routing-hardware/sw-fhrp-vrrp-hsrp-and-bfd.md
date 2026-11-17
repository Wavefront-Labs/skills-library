---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-fhrp-vrrp-hsrp-and-bfd
name: sw-fhrp-vrrp-hsrp-and-bfd
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [fhrp-vrrp-hsrp, bfd-fast-failover, gateway-redundancy, sw-high-availability]
level: practitioner
status: draft
description: "Configure VRRP or HSRP with tracking and preemption and use BFD for sub-second failure detection of links and routing neighbours."
sources:
  - https://www.rfc-editor.org/rfc/rfc5798
  - https://www.rfc-editor.org/rfc/rfc5880
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FHRP and BFD

- VRRP (open standard, RFC 5798) and HSRP (Cisco) share a virtual IP/MAC between routers; one is active/master. GLBP load-balances but is Cisco-only and rarely used.
- Set priority, enable preemption deliberately, and track an uplink or route so a router that lost its upstream gives up mastership.
- Tune hello/hold timers cautiously; faster timers raise CPU and flap risk.
- BFD runs lightweight hellos (tens to hundreds of ms) to detect forwarding failures faster than protocol timers; attach it to BGP/OSPF/static routes.
- In anycast-gateway fabrics (EVPN) FHRP is not needed.

## Verify
- [ ] Failover test (shut the master uplink) moves the virtual IP and traffic recovers within the expected time.
