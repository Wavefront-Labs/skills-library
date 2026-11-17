---
id: computing-software.systems-network-administration.cisco-networking.interface-error-counters
name: interface-error-counters
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, interface-errors, interface-counters, crc-errors, input-errors, runts-giants, output-drops, input-queue-drops, clear-counters, show-interfaces, show-interfaces-counters-errors, fcs-err, physical-layer-troubleshooting]
level: practitioner
status: draft
description: "Read Cisco interface counters correctly: CRC/FCS, runts, giants, input/output drops, what each points to (cable, optic, MTU, congestion) and how to measure rates, not totals."
sources:
  - https://www.cisco.com/c/en/us/support/docs/interfaces-modules/port-adapters/12768-eth-collisions.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interface error counters

Totals since the last clear mean nothing on their own. Always clear, wait, re-read, or compare
two snapshots N minutes apart.

## Commands
```
show interfaces Gi1/0/24                       ! full counters + 5-min rates
show interfaces Gi1/0/24 counters errors       ! Align-Err FCS-Err Xmit-Err Rcv-Err UnderSize OutDiscards
show interfaces counters errors               ! (switch) every port in one table
show controllers ethernet-controller Gi1/0/24  ! per-MAC detail on Catalyst
clear counters Gi1/0/24
```
Check `Last clearing of "show interface" counters` before drawing any conclusion.

## What each counter means
| Counter | Meaning | Usual cause |
|---|---|---|
| CRC / FCS-Err | frame failed checksum on receive | bad cable/patch, dirty or failing optic, EMI, duplex mismatch (with late collisions on the other side) |
| Runts / UnderSize | < 64 bytes with bad CRC | collisions on half duplex, faulty NIC |
| Giants | > max frame size | MTU mismatch (jumbo sender), sometimes 802.1Q/MPLS overhead on old hardware |
| Input errors | sum of runts, giants, CRC, frame, overrun, ignored | look at the components |
| Overrun / ignored | hardware could not take the frame | CPU/ASIC busy, microbursts |
| Input queue drops | punted traffic dropped at the CPU queue | traffic to the CPU (ARP storm, routing protocol flood); `show interfaces` "Input queue: x/75/drops" |
| Output drops / OutDiscards | egress buffer full | congestion, speed mismatch (10G into 1G), microbursts; QoS queue tuning |
| Late collisions | collision after 64 bytes | duplex mismatch or cable over spec length |

Rule of thumb: CRC errors are counted on the **receiving** side; the fault is often the far
end's transmitter, its optic, or the cable between. Swap one component at a time.

## Workflow
1. Snapshot `show int` on both ends; note speed/duplex and media type.
2. `clear counters`, generate load, re-check after 5-10 min.
3. CRC increasing: reseat/replace patch lead, clean and check optics (DOM levels), try another
   port to split port vs cable.
4. Output drops only: check `show interfaces Gi1/0/24 | i rate|drops` and QoS
   (`show platform hardware fed switch active qos queue stats interface Gi1/0/24` on C9K).

## Gotchas
- Errors at a rate below 1 in 10^6 frames are often background; trend them, do not chase them.
- `clear counters` also resets the SNMP view on some platforms and breaks rate graphs for one poll.
- Giants on a trunk with baby-giant frames (QinQ) may be harmless; check `system mtu`.

## Verify
- [ ] After the fix, CRC count stays flat over a busy period.
- [ ] Both ends show the same speed/duplex and no late collisions.
- [ ] Output drops correlate (or not) with utilisation in your monitoring graphs.
