---
id: computing-software.systems-network-administration.cisco-networking.interface-flapping-and-carrier-delay
name: interface-flapping-and-carrier-delay
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, interface-flapping, carrier-delay, link-debounce, updown, link-flap, dampening, troubleshooting]
level: practitioner
status: draft
description: "Diagnose and contain flapping links: find flaps in logs and counters, separate physical from protocol causes, and tune carrier-delay, link debounce and IP event dampening."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/configuration/xe-16/iri-xe-16-book/iri-ip-event-damp.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interface flapping

A flapping link causes routing churn, STP topology changes and MAC flushes far beyond the port
itself. Find the cause first; dampen only to protect the network while you fix it.

## Find the flaps
```
show logging | include UPDOWN|LINK-3
show interfaces Gi1/0/24 | include line protocol|Last input|carrier transitions|resets
show interfaces Gi1/0/24 counters errors
show controllers ethernet-controller Gi1/0/24 phy | include Link|Speed   ! platform dependent
```
`%LINK-3-UPDOWN` = physical (carrier) change. `%LINEPROTO-5-UPDOWN` without LINK = keepalive or
protocol (e.g. UDLD, LACP, PPP) issue. A rising `carrier transitions` counter confirms physical.

## Typical causes by pattern
| Pattern | Likely cause |
|---|---|
| Flaps every few seconds, CRC errors | bad cable/patch, dirty fibre, marginal optic (check DOM) |
| Flaps with PoE device reboots | power budget, PD drawing over class |
| Flaps at fixed intervals (e.g. 30 s) | keepalive/UDLD/LACP timeout, far-end NIC power saving |
| Only line protocol | encapsulation/keepalive mismatch on serial/tunnel |
| Many ports at once | upstream device, power event, stack issue |

Swap one variable at a time: patch lead, then optic, then port, then far-end NIC.

## Containment knobs
```
interface TenGigabitEthernet1/1/1
 carrier-delay msec 0        ! report down immediately (fast failover on routed links)
 carrier-delay up 2          ! wait before declaring up (hold down on unstable circuits)
 link debounce time 100      ! Catalyst: ignore sub-100 ms carrier blips (platform dependent)
 dampening 5 1000 2000 20    ! IP event dampening: half-life restart suppress max-suppress
show dampening interface
show interfaces dampening
```
IP event dampening keeps a flapping interface down for routing protocols (penalty accumulates per
flap and decays) so OSPF/EIGRP do not recompute every flap.

## Gotchas
- `carrier-delay` defaults vary by platform (often 2 s on routers, 0 on switches); on a WAN circuit
  with BFD, keep it at 0 down and let BFD handle detection.
- Dampening hides the symptom: monitoring must alert on `%IP_DAMPENING` or interface suppression.
- Energy Efficient Ethernet and NIC power management on hosts cause periodic flaps; disable EEE on
  the port to test.
- errdisable `link-flap` will shut the port after 5 flaps in 10 s; check `show errdisable flap-values`.

## Verify
- [ ] Carrier transitions stop incrementing after the fix over 24 h.
- [ ] No UPDOWN messages and routing neighbours stable (`show ip ospf neighbor` uptime).
