---
id: computing-software.systems-network-administration.cisco-networking.hsrp-state-troubleshooting
name: hsrp-state-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, hsrp, hsrp-troubleshooting, hsrp-states, dual-active, virtual-mac, fhrp, duplicate-address]
level: practitioner
status: draft
description: "Troubleshoot HSRP: both routers active, constant state changes, version/group mismatches, duplicate-address warnings, and hosts using the wrong gateway MAC."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/hot-standby-router-protocol-hsrp/10583-62.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp_fhrp/configuration/xe-16/fhp-xe-16-book/fhp-hsrp.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HSRP state troubleshooting

## Read the state
```
show standby brief
!  Interface Grp Pri P State   Active        Standby       Virtual IP
!  Vl10      10  110 P Active  local         10.10.0.3     10.10.0.1
show standby Vlan10
show logging | include HSRP
```
States: Init -> Learn -> Listen -> Speak -> Standby -> Active. In a healthy pair one is Active and
one Standby; any extra routers are Listen.

## Both routers Active (split brain)
They cannot hear each other's hellos (224.0.0.2 v1, 224.0.0.102 v2, UDP 1985). Causes:
- L2 path broken between them: VLAN not on the trunk, STP blocking, port-channel down.
- ACL or CoPP dropping UDP 1985.
- Version mismatch: one v1, one v2 (different multicast group and virtual MAC).
- Group number or authentication mismatch (`%HSRP-4-BADAUTH`).
Effect: two routers answering ARP for the gateway with the same virtual MAC; MAC flapping on
switches and intermittent loss.

## Constant flapping
- Hello/hold timers too aggressive for the CPU, or hellos lost under congestion.
- Object tracking toggling (unstable tracked interface or IP SLA). Check `show track`.
- Preempt plus a delay too short after reload (router becomes active before its routing converges):
  `standby 10 preempt delay minimum 60`.

## Duplicate address warnings
`%HSRP-4-DUPADDR: Duplicate address 10.10.0.1 on Vlan10, sourced by 0000.0c07.ac0a`. Another
device owns the virtual IP, or a loop reflects your own hellos back. Check for a static IP on a
host and for L2 loops (`show mac address-table address 0000.0c07.ac0a`).

## Virtual MACs
- v1: 0000.0c07.acXX (XX = group in hex, 0-255).
- v2: 0000.0c9f.fXXX (groups 0-4095).
- IPv6 (v2 only): 0005.73a0.0XXX.
Hosts should have the virtual MAC in their ARP cache for the gateway; a physical MAC means a
misconfigured host gateway or proxy ARP answering.

## Verify
- [ ] One Active, one Standby, stable `Last state change` timestamps.
- [ ] Failover test: shut the active's uplink (tracked) and confirm the standby takes over within
  hold time.
