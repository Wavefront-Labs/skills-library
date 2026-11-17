---
id: computing-software.systems-network-administration.wireshark.broadcast-and-multicast-capture-filters
name: broadcast-and-multicast-capture-filters
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, capture-filters, broadcast-filter, multicast, bpf]
level: practitioner
status: verified
description: "Isolate or exclude broadcast and multicast traffic with capture filters and display filters, and measure broadcast storms per source."
sources:
  - https://www.tcpdump.org/manpages/pcap-filter.7.html
  - https://www.wireshark.org/docs/dfref/e/eth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broadcast and multicast filters

## Capture filters
```
broadcast                     # Ethernet broadcast (ff:ff:ff:ff:ff:ff)
multicast                     # Ethernet multicast incl. broadcast
ether broadcast or ether multicast
ip broadcast                  # needs netmask on some platforms; use dst host 255.255.255.255
ip multicast                  # 224.0.0.0/4
ip6 multicast                 # ff00::/8
not broadcast and not multicast   # unicast only: big reduction on noisy access VLANs
```
`ip broadcast` checks subnet-directed broadcasts using the capturing interface netmask; with no
address configured it compiled to a test for destination 0.0.0.0 or 255.255.255.255 only, so use
`dst host 255.255.255.255 or dst net 10.1.1.255/32` explicitly. (All capture filters here were compiled with
`dumpcap -d` and run against a synthetic capture.)

## Display filters
```
eth.dst == ff:ff:ff:ff:ff:ff
eth.dst.ig == 1               # group bit: multicast or broadcast
ip.dst == 224.0.0.0/4
ipv6.dst == ff02::/16
```

## Broadcast storm triage
1. Capture 10 seconds on an access port with `broadcast or multicast`.
2. Statistics > Endpoints > Ethernet, sort by Packets: one MAC sending thousands per second is the
   loop or the broken NIC.
3. Statistics > Protocol Hierarchy shows which protocol (ARP, SSDP, mDNS, NetBIOS, LLMNR).
4. `tshark -r b.pcap -q -z io,stat,1,"eth.dst.ig==1"` gives broadcasts per second. Compare with the VLAN's
   normal baseline (rule of thumb, no standard threshold); thousands per second of identical frames suggests a loop.

## Gotchas
- A capture on one switch port only shows what the switch forwards to that port; seeing no multicast does not
  prove none exists elsewhere.

## Verify
- [ ] Endpoint counts before and after the fix show the offending MAC gone or under baseline.
