---
id: computing-software.systems-network-administration.cisco-networking.decoding-erspan-at-the-collector
name: decoding-erspan-at-the-collector
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, erspan-decode, erspan, gre, wireshark, tcpdump, erspan-type-ii, erspan-type-iii, traffic-mirroring, cisco-ios]
level: practitioner
status: draft
description: "Receive and decode ERSPAN on a Linux or Wireshark collector: GRE protocol types for Type II/III, session IDs, stripping headers, and capture filters."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_erspan.html
  - https://datatracker.ietf.org/doc/html/draft-foschiano-erspan-03
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decoding ERSPAN at the collector

## On the wire
ERSPAN = original frame + ERSPAN header + GRE + outer IP to the collector.
| Type | GRE protocol | ERSPAN header | Notes |
|---|---|---|---|
| Type I | 0x88BE | none | legacy |
| Type II | 0x88BE | 8 bytes (session ID 10 bits, VLAN, CoS) | most common |
| Type III | 0x22EB | 12+ bytes, timestamps, optional platform subheader | Nexus, newer platforms |

The collector needs no tunnel config to receive: packets arrive as GRE (IP protocol 47) to its IP.

## Capture
```
tcpdump -i eth1 -w erspan.pcap 'ip proto 47'
tcpdump -i eth1 'ip proto 47 and host 10.0.0.1'      # from a specific source switch
```
Wireshark decodes ERSPAN automatically (GRE -> ERSPAN -> Ethernet). Filters: `erspan.spanid == 10`,
`erspan` to show only ERSPAN, and inner fields as normal (`ip.addr == 10.10.0.20`).
If Wireshark shows only GRE with unknown payload, check Decode As (GRE protocol 0x88BE -> ERSPAN)
and the "Assume ERSPAN Type I if no header" preference for Type I.

## Strip headers for tools that cannot read ERSPAN
- `editcap -C 50 in.pcap out.pcap` crudely chops a fixed outer length (14 Ethernet + 20 IP + 8 GRE w/ seq + 8 ERSPAN II = 50 bytes).
- Linux kernel: create an `erspan` interface (`ip link add erspan1 type erspan seq key 10 local <COLLECTOR> remote <SWITCH> erspan_ver 1`) and capture on it to get decapsulated frames.

## Gotchas
- MTU: mirrored 1500-byte frames + ~50 bytes overhead; switches truncate or fragment. Raise MTU
  on the path or set `mtu` in the ERSPAN session.
- Sequence numbers missing = drops in transit; ERSPAN has no retransmission.
- Firewalls must permit GRE to the collector; NAT of GRE is unreliable.
- Session ID in the switch config (`erspan-id 10`) helps separate multiple sources.

## Verify
- [ ] `tshark -r erspan.pcap -Y erspan -T fields -e erspan.spanid | sort | uniq -c` shows expected session IDs.
