---
id: computing-software.systems-network-administration.cisco-networking.mac-flapping-and-unicast-flooding
name: mac-flapping-and-unicast-flooding
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, mac-learning, mac-address-table, mac-flapping, mac-move, unknown-unicast-flooding, macflap-notif, layer-2-loop, unicast-flooding, storm-control, nic-teaming]
level: practitioner
status: draft
description: "Diagnose %SW_MATM-4-MACFLAP_NOTIF and unknown-unicast flooding: tell a Layer 2 loop from NIC teaming or a VM move, trace the ports and stop the flood safely."
sources:
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/116251-trouble-macflap-00.html
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6000-series-switches/23563-143.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MAC flapping and unknown-unicast flooding

## Read the message
```
%SW_MATM-4-MACFLAP_NOTIF: Host 0050.5699.1a2b in vlan 30 is flapping between port Gi1/0/1 and port Po1
```
The same source MAC arrived on two ports. Find out why before you shut anything.

## Causes, in order of danger
| Cause | Tells |
|---|---|
| Layer 2 loop | many MACs flapping at once, CPU high, broadcast counters exploding, STP TCNs |
| Unmanaged switch/hub looped on an access port | flaps between an access port and an uplink, BPDU guard absent |
| NIC teaming/bonding in a mode the switch is not configured for (balance-alb, switch-independent with same MAC) | one or two server MACs, steady low-rate flapping between two server ports |
| VM vMotion / failover | one-time move, not repeated |
| FHRP/VRRP misconfig, two active routers | flap of the virtual MAC (0000.0c07.acXX, 0000.5e00.01XX) |

## Investigate
```
show mac address-table address 0050.5699.1a2b
show logging | i MACFLAP
show spanning-tree detail | i ieee|occurr|from|is exec   ! topology change counts and source port
show interfaces | i is up|broadcasts                    ! broadcast rates
show processes cpu sorted | ex 0.00
```
Follow the "from" port of the last topology change downstream until you find the looped
device. Use `show cdp neighbors` to walk switches.

## Stop a loop now
1. Shut the access port flagged in the flap (or the downstream port of the last TCN).
2. If you cannot reach the switch, shut the uplink toward it from the distribution layer.
3. Then fix: PortFast + BPDU Guard on access ports, storm control
   (`storm-control broadcast level 1.00` `storm-control action trap`), loop guard on uplinks.

## Unknown-unicast flooding without flapping
- ARP timeout > MAC aging with asymmetric routing (see mac-address-table-aging-and-static).
- Table full: `show mac address-table count`.
- STP topology changes flush tables to 15 s aging repeatedly: find the flapping edge port that
  lacks PortFast.
- Optional: `switchport block unicast` on ports that never need unknown unicast.

## Gotchas
- Teaming: either configure an EtherChannel (LACP) toward the server, or use a teaming mode
  that sends each MAC out one NIC only. Do not "fix" with `no mac address-table notification`.
- Some platforms err-disable flapping ports (`mac address-table notification mac-move` action
  varies); know your platform before enabling.

## Verify
- [ ] No new MACFLAP messages for an hour.
- [ ] Topology change count on the core stops increasing.
- [ ] Broadcast rate on uplinks back to baseline.
