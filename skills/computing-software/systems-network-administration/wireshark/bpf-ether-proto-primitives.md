---
id: computing-software.systems-network-administration.wireshark.bpf-ether-proto-primitives
name: bpf-ether-proto-primitives
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, capture-filters, bpf, ether-proto, pcap-filter, arp]
level: practitioner
status: verified
description: "Write capture filters with link and protocol primitives: ether proto, ether host, arp, icmp, ip proto and vlan, including the vlan keyword offset trap."
sources:
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
  - https://wiki.wireshark.org/CaptureFilters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BPF ether proto and protocol primitives

Capture filters (pcap-filter syntax) run in the kernel before packets are copied, so they are the
way to keep busy links from overwhelming the capture.

## Link layer
```
ether host 00:11:22:33:44:55
ether src 00:11:22:33:44:55
ether proto 0x88cc          # LLDP
ether proto 0x8100          # 802.1Q tagged (prefer the vlan keyword)
ether proto 0x888e          # EAPOL
ether[0] & 1 = 1            # multicast/broadcast destination
```
Shorthands: `arp`, `rarp`, `ip`, `ip6`, `stp`, `ether proto \arp` (backslash because `arp` is also a
keyword).

## Network/protocol
```
icmp                        # IPv4 ICMP only
icmp6
ip proto 47                 # GRE
ip proto \tcp
icmp[icmptype] == icmp-echo or icmp[icmptype] == icmp-echoreply
ip6 and ip6[6] == 58        # ICMPv6 without extension headers
```

## VLAN-tagged traffic
`vlan` changes the offsets of everything after it in the expression.
```
vlan and host 10.1.1.5          # matches tagged packets only (also tagged ARP for that host)
host 10.1.1.5 or (vlan and host 10.1.1.5)   # tagged and untagged
vlan 20 and arp
```
Put `vlan` first: `host 10.1.1.5 and vlan` is rejected by the Npcap/libpcap in Wireshark 4.4.1
("isn't a valid capture filter (expression rejects all packets)"). On Linux the NIC may strip the tag before
libpcap sees it (VLAN offload); turn that offload off in the driver settings to keep tags.
Every filter on this page was compiled with `dumpcap -d` and the compiled program was run against a synthetic
capture of tagged, untagged, ARP, ICMPv6, LLDP and EAPOL frames; each matched the intended frames.

## Test
```
dumpcap -i eth0 -f "ether proto 0x88cc" -d     # print compiled BPF, error if invalid
dumpcap -i 1 -f "vlan and arp" -d              # `-d` prints the BPF program; `-i` is required
```

## Verify
- [ ] Capture a few seconds and check every packet in the file matches the intended protocol.
