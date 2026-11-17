---
id: computing-software.systems-network-administration.cisco-networking.stp-topology-change-and-loop-troubleshooting
name: stp-topology-change-and-loop-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, spanning-tree, stp, rapid-pvst, topology-change, tcn, stp-loop, layer-2-loop, broadcast-storm, show-spanning-tree-detail, mac-flapping, portfast]
level: practitioner
status: docs-checked
description: "Trace frequent STP topology changes to the flapping port and find and break a live Layer 2 loop: TC counters, source port walk, loop symptoms, safe containment."
sources:
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/28943-170.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/24062-146.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/10556-16.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Topology changes and STP loops

## Topology changes (TCs)
A topology change makes switches shorten or flush their MAC tables so stale entries do not
black-hole traffic; unknown destinations are then flooded until relearned. In RSTP only a
non-edge port moving to forwarding causes a TC (a port going to blocking no longer does), and the
switch that detects it floods the TC and clears the MACs learned on all its other ports. Ports
with PortFast do not cause TCs when they go to or from forwarding. A TC is a rare event in a
well-configured network, so a counter that keeps climbing means a flapping port, usually an edge
port without PortFast. Repeated TCs at short intervals mean near-constant flooding.

### Find the source
```
show spanning-tree vlan 10 detail
! VLAN0010 is executing the rstp compatible Spanning Tree protocol
!   Number of topology changes 4512 last change occurred 00:00:41 ago
!           from GigabitEthernet1/0/48
```
Start at the STP root bridge for that VLAN: in Cisco IOS the counter increments only when a TCN
BPDU is received, so the root has the most accurate count. Go to the device on the "from" port
(CDP/LLDP), run the same command, and repeat until the "from" port is a local access port or a
flapping link. Then:
- Port without PortFast facing an end device: add `spanning-tree portfast` (only on
  end-station ports).
- Flapping link: check errors and optics (`show interfaces`, `show logging`).
- `debug spanning-tree events` briefly if still unclear, with `logging buffered` and console or
  out-of-band access; watch CPU and turn debug off afterwards. In MST mode that command does not
  work; use `debug spanning-tree mstp roles` for role changes.

## A live loop
Symptoms seen together point to a forwarding loop: loss of connectivity through the affected
region, links at or near 100 percent utilisation, high CPU on routers (routing neighbour or HSRP
flapping), MAC flapping or constant relearning syslogs, output drops rising on many interfaces.

Containment:
1. Use the console or out-of-band access (remote sessions probably fail during a loop).
2. Find the busiest ports with `show interface | include line|\/sec` (packets per second).
   Ports that sustain the loop sit on the redundant path; ports that merely flood the looped
   traffic show high rates but shutting them barely helps.
3. Shut one suspect redundant path at a time, preferably at the distribution or core switch, and
   check utilisation and connectivity after each. The port whose shutdown ends the loop marks the
   redundant path where STP failed. Disconnecting the link works if you have no CLI.
4. Collect information before reloading switches, or the root cause is lost.
5. Check that every switch on the redundant path agrees on the root (`show spanning-tree vlan N`),
   and that blocked ports still receive BPDUs (`show spanning-tree interface X detail`, BPDU
   received counter should climb).

Common causes Cisco lists: unidirectional links (bad transceiver or fibre), duplex mismatch,
BPDU loss from corruption or overloaded CPU, PortFast on a port that connects to a hub or
bridge, aggressive timer tuning, and STP disabled on a VLAN. Never disable STP, even if no
ports block.

## Prevent
UDLD on switch-to-switch links, loop guard on all switches (use both), PortFast on end-station
ports with BPDU guard, root guard where outside influence is possible, keep default STP timers,
and keep user traffic off the management VLAN.

## Verify
- [ ] Topology change count stops increasing (check twice, minutes apart).
- [ ] CPU and link utilisation are back to baseline.
- [ ] The offending port has PortFast and BPDU guard, and the device was removed or fixed.

## Checked
2026-11-08. Confirmed against the three cited Cisco pages (Troubleshoot STP Issues on Catalyst
Switches, Understand Rapid Spanning Tree Protocol (802.1w), Troubleshoot STP Problems and
Related Design Considerations): TC triggers and MAC flushing, PortFast not causing TCs, the
detail output fields, the TCN-only counter note, loop symptoms, port-by-port shutdown, debug
commands and MST variant, prevention list. Removed unsupported specifics: "a few TCs a day",
LED and broadcast-count signs, unmanaged-switch, server-bridge and EtherChannel mode on causes,
storm control and syslog alert advice. The first source page, 12013-17, now returns a retired
products index and was replaced.
Method: documentation only; no commands were run.
