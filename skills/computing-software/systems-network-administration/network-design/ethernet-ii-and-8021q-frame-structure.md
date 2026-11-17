---
id: computing-software.systems-network-administration.network-design.ethernet-ii-and-8021q-frame-structure
name: ethernet-ii-and-8021q-frame-structure
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ethernet-frame, ethernet-ii, 802-1q, ethertype, vlan-tag, fcs, osi-model]
level: practitioner
status: gated
description: "Read Ethernet II and 802.1Q frames field by field: preamble, MACs, TPID/TCI, EtherType vs length, FCS, minimum/maximum sizes and what each means when troubleshooting."
sources:
  - https://standards.ieee.org/ieee/802.1Q/10323/
  - https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml
  - https://wiki.wireshark.org/Ethernet
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ethernet II and 802.1Q frame structure

## Layout on the wire
Checked against the Linux headers (`ETH_HLEN` 14, `ETH_ZLEN` 60 without FCS, `ETH_DATA_LEN` 1500, `ETH_FCS_LEN` 4, `ETH_P_802_3_MIN` 0x0600, the TCI masks PCP `0xe000`, DEI `0x1000`, VID `0x0fff`) and with scapy/tshark; the I/G bit rows were confirmed by `eth.ig == 1` matching broadcast and LLDP multicast frames.
| Field | Bytes | Notes |
|---|---|---|
| Preamble + SFD | 7 + 1 | `0x55...55D5`; stripped by the NIC, never seen in captures |
| Destination MAC | 6 | I/G bit (LSB of first octet) = 1 means group (multicast/broadcast) |
| Source MAC | 6 | U/L bit (second LSB) = 1 means locally administered (random/VM MACs) |
| 802.1Q tag (optional) | 4 | TPID `0x8100` + TCI: PCP 3 bits, DEI 1 bit, VID 12 bits |
| EtherType / Length | 2 | >= `0x0600` (1536) = EtherType; <= 1500 = 802.3 length + LLC follows |
| Payload | 46-1500 | padded to 46 (42 when tagged) so the frame reaches 64 bytes |
| FCS | 4 | CRC-32; usually stripped before the capture driver |

Frame sizes: minimum 64 bytes (header + payload + FCS), maximum 1518 untagged, 1522 tagged
("baby giant"). Q-in-Q adds a second tag with TPID `0x88A8` (802.1ad S-tag) -> 1526.

## EtherTypes to recognise
`0x0800` IPv4, `0x86DD` IPv6, `0x0806` ARP, `0x8100` 802.1Q, `0x88A8` 802.1ad, `0x8847` MPLS
unicast, `0x88CC` LLDP, `0x888E` 802.1X EAPOL, `0x8809` LACP/slow protocols, `0x88F7` PTP.

## VID values
VID 0 = priority-tagged (PCP only, no VLAN) and PCP 5 for voice (gated: unconfirmed, source is paywalled or blocked: IEEE 802.1Q). VID 4095 is reserved: the Linux 8021q netlink code rejects a VLAN id of 4095 or more, so usable IDs are 1-4094. PCP carries CoS 0-7.

## Troubleshooting with frame fields
- Runts (< 64 bytes) and CRC/FCS errors on a port: duplex mismatch, bad cable/optic, EMI.
- Giants: tagged frames arriving on a port that does not accept 1522, or jumbo frames on a
  1500 port. Check the interface error counters and the MTU on both ends.
- Wireshark shows no 802.1Q tag on a trunk: the NIC/driver strips tags (VLAN offload). Disable
  rx-vlan offload (`ethtool -K eth0 rxvlan off`; the ethtool man page lists `rxvlan`) or capture with a TAP.
- Display filters: `eth.dst == ff:ff:ff:ff:ff:ff`, `vlan.id == 20`, `eth.type == 0x88cc`,
  `eth.ig == 1` (group addresses).

## Verify
- [ ] You can name each field in a captured frame and say whether it is tagged, unicast/multicast, and which EtherType follows.
