---
id: computing-software.systems-network-administration.wireshark.encapsulated-traffic-capture-filters
name: encapsulated-traffic-capture-filters
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, capture-filters, encapsulated-traffic-filter, mpls, gre, vxlan, bpf]
level: practitioner
status: verified
description: "Filter traffic inside MPLS, GRE, VXLAN and Geneve tunnels with BPF offsets and display filters when plain host/port filters miss inner packets."
sources:
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
  - https://www.wireshark.org/docs/dfref/v/vxlan.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Filtering encapsulated traffic

`host 10.1.1.5` matches the outer header only. Inner packets of tunnels need special handling.

## MPLS
```
mpls                                  # any labelled packet; shifts offsets like vlan
mpls 100                              # top label 100
mpls and host 10.1.1.5                # inner IP after one label
mpls and mpls and host 10.1.1.5       # two labels (L3VPN)
```
(Run: `mpls 100` and `mpls and host 10.1.1.5` matched the one-label packet; the two-label filter matched only the
two-label packet.)

## GRE
Inner IPv4 starts at offset 24 of the outer IP for plain GRE (20 IP + 4 GRE):
```
ip proto 47 and ip[24+12:4] == 0x0a010105    # inner src 10.1.1.5
ip proto 47 and ip[24+16:4] == 0x0a010105    # inner dst
```
(Run: the inner-src filter matched a GRE packet carrying 10.1.1.5 and the inner-dst filter did not.)
GRE with key/sequence options adds 4 bytes each (RFC 2890: Key and Sequence Number fields are 4 octets); check the GRE
flags in one packet first.

## VXLAN (UDP 4789) and Geneve (UDP 6081)
Inner Ethernet starts after 8-byte UDP + 8-byte VXLAN header. Using `udp[]` offsets:
```
udp dst port 4789 and udp[8+4:4] == 0x00138800   # VNI 5000 (BPF loads are 1, 2 or 4 bytes: udp[12:3] is rejected)
udp port 4789 and udp[16+12:2] == 0x0800 and udp[16+14+12:4] == 0x0a010105
```
(16 = UDP 8 + VXLAN 8; inner Ethernet 14 bytes; inner IP src at +12.) Both VXLAN filters matched a synthetic
VNI 5000 packet. The libpcap in Wireshark 4.4.1 compiles the `geneve` keyword.

## Display filters are simpler
```
vxlan.vni == 5000 && ip.addr == 10.1.1.5      # matches inner or outer ip.addr
ip.src == 10.1.1.5 && gre
mpls.label == 100
```
Wireshark has multiple `ip` layers per frame; use the layer operator `ip.src#2 == 10.1.1.5` to
target the inner header only. Non-standard VXLAN ports need Decode As (UDP port > VXLAN).

## Verify
- [ ] Compile with `dumpcap -d -f "<filter>"` and confirm a short capture contains only inner-host packets.
