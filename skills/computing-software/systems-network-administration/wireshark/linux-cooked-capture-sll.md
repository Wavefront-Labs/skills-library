---
id: computing-software.systems-network-administration.wireshark.linux-cooked-capture-sll
name: linux-cooked-capture-sll
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcpdump, linux-cooked-capture, sll, sll2, any-interface, link-layer-type]
level: practitioner
status: verified
description: "Work with captures from the Linux any interface: SLL vs SLL2 headers, packet type and interface fields, missing MACs, and filtering when the link layer is cooked."
sources:
  - https://www.tcpdump.org/linktypes/LINKTYPE_LINUX_SLL.html
  - https://www.tcpdump.org/linktypes/LINKTYPE_LINUX_SLL2.html
  - https://wiki.wireshark.org/SLL
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux cooked capture (SLL / SLL2)

`tcpdump -i any` and `dumpcap -i any` cannot use a real link-layer header because interfaces
differ (Ethernet, tunnel, PPP). libpcap writes a synthetic "cooked" header instead.

## SLL (LINKTYPE_LINUX_SLL, 113) fields
- Packet type: `0` sent to us by somebody else, `1` broadcast, `2` multicast (not broadcast), `3` sent to somebody else by
  somebody else, `4` sent by us (outgoing). Very useful to tell direction.
- ARPHRD type, link-layer address length and address (the source MAC, if any), protocol.
- No destination MAC, no interface name.

## SLL2 (LINKTYPE_LINUX_SLL2, 276), libpcap 1.10+
Adds the interface index (4 octets), so Wireshark shows `sll.ifindex`. libpcap 1.10.0 added DLT_LINUX_SLL2 and tcpdump 4.99.0 made
SLL2 the default for the Linux `any` device; select a link type with `tcpdump -y <type>`.

## Filtering
Display filters:
```
sll.pkttype == 4            # outgoing only
sll.pkttype == 0            # incoming unicast
sll.ifindex == 3
```
Capture filters work on IP/TCP as usual (`host 10.0.0.5 and port 443`); `ether host` filters do
not apply because there is no Ethernet header.

## Why use it
- Finding which interface traffic uses on a multi-homed host, a host with VLAN subinterfaces, or a
  Kubernetes node (veths, flannel/cilium devices).
- Seeing both the encapsulated and decapsulated forms of tunnel traffic in one file (packets appear
  on both the physical and tunnel interface).

## Gotchas
- Duplicates: a packet routed through the host (or bridged) appears once per interface it crosses.
  Filter by ifindex or use editcap -d carefully (not true duplicates; timestamps and headers differ).
- No VLAN tags or MACs for L2 troubleshooting; capture on the physical interface for that.
- A Wireshark too old to know link type 276 cannot decode SLL2; use a current release.
- Merging an SLL capture with Ethernet captures needs pcapng (mixed link types).

## Verify
- [ ] Add `sll.pkttype` and `sll.ifindex` columns; direction and interface are visible per packet.

## Checked (2026-10-22)
- Wrote SLL (link type 113) and SLL2 (276) captures with scapy and opened them in Wireshark 4.4.1: SLL packet types 0, 4 and 3 decoded per packet and `sll.pkttype == 4`/`== 0` filtered them, SLL2 frames with ifindex 3 and 5 filtered with `sll.ifindex == 3`; `sll.pkttype`, `sll.ifindex` and `sll.ltype` exist in `tshark -G fields`.
- Link-type numbers and header layouts (packet type 0-4 meanings, 8-octet source address, no destination MAC, SLL2 interface index) read at https://www.tcpdump.org/linktypes/LINKTYPE_LINUX_SLL.html and https://www.tcpdump.org/linktypes/LINKTYPE_LINUX_SLL2.html (113 and 276); libpcap CHANGES lists "Add DLT_LINUX_SLL2" under the 1.10.0 summary and tcpdump CHANGES lists "Make SLL2 the default for Linux any pseudo-device" under 4.99.0.
- Not run: `dumpcap -i any`/`tcpdump -i any` themselves (no Linux host) and the multi-interface duplicate behaviour (interpretation); `editcap -d` on such duplicates is untested.
