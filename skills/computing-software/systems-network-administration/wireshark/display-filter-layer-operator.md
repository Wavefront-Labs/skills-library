---
id: computing-software.systems-network-administration.wireshark.display-filter-layer-operator
name: display-filter-layer-operator
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, display-filter, layer-operator, tunnel-analysis, vxlan, gre, ipsec, encapsulation]
level: practitioner
status: verified
description: "Filter on inner or outer headers of tunnelled traffic with the display filter layer operator (#), plus custom columns and occurrence selection for VXLAN, GRE and IP-in-IP."
sources:
  - https://www.wireshark.org/docs/man-pages/wireshark-filter.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layer operator for tunnelled fields

A VXLAN, GRE or IP-in-IP packet contains two (or more) IP headers. `ip.src == x`
matches either. Wireshark 4.0+ lets you select which layer.

## Syntax
```
ip.src#1 == 192.0.2.10        # outer IP header (first occurrence of the ip protocol layer)
ip.src#2 == 10.20.0.5         # inner IP header
tcp.port#1 == 443             # only if TCP appears once anyway
ip.addr#2 == 10.20.0.0/16
```
Ranges: `ip.addr#[2-3]` (layers 2 to 3). Negative layer numbers such as `#-1` are a syntax error in 4.4.1; count from
the outside. The protocol name itself takes a layer too: `ip#2` (a second IP header exists), `eth#2`, `eth.src#2 == 02:00:00:00:00:01`.

## Typical uses
- Underlay vs overlay in VXLAN: outer `ip#1` = VTEPs, inner `ip#2` = tenant hosts.
  `udp.dstport == 4789 && ip.addr#2 == 10.20.0.5`
- GRE (`ip.src#1 == 192.168.1.1`, `ip.src#2 == 172.16.0.1` matched the same GRE test packet) and other IP-in-IP encapsulations.
- ICMP errors embed the original IP header: `ip.dst#2` is the original destination that failed.

## Occurrence selection without the layer operator
In tshark, `-e ip.src -E occurrence=l` prints the last (inner) occurrence and `occurrence=f` the first (checked on a
VXLAN packet: inner 10.20.0.5 vs outer 192.0.2.10). Add both outer and inner columns when analysing overlays.

## Older Wireshark (3.x)
No layer operator (the 4.0.0 release notes list it as new). Use occurrence-based custom columns instead.

## Gotchas
- Layer numbering is per protocol name: `eth#2` is the inner Ethernet in VXLAN, `ip#2` the inner IP (confirmed on a
  VXLAN packet and on an ICMP error carrying the original IP header, where `ip.dst#2` is that header's destination).
- Decode As may be needed so the tunnel payload is dissected at all: VXLAN on UDP 5000 gave no `ip.addr#2` match until
  `tshark -d udp.port==5000,vxlan` was added.

## Verify
- [ ] Packet count for `ip.addr#2 == host` equals the conversations you expect from that inner host
  and excludes underlay traffic.
