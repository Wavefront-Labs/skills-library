---
id: computing-software.systems-network-administration.cisco-networking.embedded-packet-capture
name: embedded-packet-capture
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, catalyst-9000, ios-troubleshooting, embedded-packet-capture, epc, monitor-capture, packet-capture, pcap, control-plane-capture, buffer-size, export-pcap, wireshark]
level: practitioner
status: draft
description: "Capture packets directly on IOS XE routers and Catalyst 9000 with monitor capture: interface or control-plane points, filters, buffer limits, exporting a pcap for Wireshark."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-embedded-packet-capture/116045-productconfig-epc-00.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_packet_capture.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Embedded Packet Capture (monitor capture)

Captures real packets on the device into a buffer and exports pcap. Use it when there is no
SPAN destination nearby or you need to see what the control plane receives.

## IOS XE (routers and Catalyst 9000)
```
monitor capture CAP interface GigabitEthernet0/0/1 both
monitor capture CAP match ipv4 host 10.20.30.40 any        ! inline filter
!   or: monitor capture CAP access-list CAP-ACL
monitor capture CAP buffer size 10                          ! MB
monitor capture CAP limit duration 120 packets 50000
monitor capture CAP start
! ... reproduce ...
monitor capture CAP stop
show monitor capture CAP buffer brief
show monitor capture CAP buffer detailed | i ^ *[0-9]|Internet
monitor capture CAP export bootflash:cap.pcap
! copy bootflash:cap.pcap scp://user@host/   then open in Wireshark
no monitor capture CAP
```
Capture point options: `interface X in|out|both`, `control-plane both` (traffic to/from the CPU:
routing protocols, SSH, punts), `vlan X` on switches.

## Classic IOS (ISR G2 and older)
```
monitor capture buffer BUF size 2048 max-size 1518 circular
monitor capture point ip cef POINT GigabitEthernet0/1 both
monitor capture point associate POINT BUF
monitor capture point start POINT
monitor capture point stop POINT
monitor capture buffer BUF export tftp://10.0.0.30/cap.pcap
```

## Tips
- Always set a filter and limits: an unfiltered capture on a 10G port fills the buffer in
  milliseconds and burns CPU on some platforms.
- Captures on Catalyst data-plane ports are done in hardware with a rate limit (often around
  1000 pps to the CPU): fine for flows, not for throughput analysis.
- `control-plane` captures are the quickest way to answer "is the router receiving the OSPF
  hellos / BGP opens / SNMP polls?"
- Combine with `debug` only when the capture alone does not explain the behaviour.

## Gotchas
- Captures stop on reload and the buffer is lost unless exported.
- Encrypted (IPsec) traffic is captured as ESP on the physical interface; capture on the tunnel
  interface to see clear text.

## Verify
- [ ] `show monitor capture CAP` shows the right point, filter and limits before starting.
- [ ] Exported pcap opens in Wireshark with the expected packets.
- [ ] Capture removed afterwards (`show monitor capture` empty).
