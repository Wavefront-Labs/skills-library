---
id: computing-software.systems-network-administration.network-design.tcp-header-and-flags
name: tcp-header-and-flags
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, tcp-header, tcp-flags, three-way-handshake, tcp-options, window-scaling, osi-model]
level: practitioner
status: verified
description: "Decode the TCP header (ports, seq/ack, flags, window, options) and read handshakes, resets and teardown in captures to pinpoint which side or middlebox broke a connection."
sources:
  - https://www.rfc-editor.org/rfc/rfc9293
  - https://www.rfc-editor.org/rfc/rfc7323
  - https://www.rfc-editor.org/rfc/rfc2018
  - https://www.wireshark.org/docs/dfref/t/tcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP header and flags

## Header (20 bytes + options, RFC 9293)
Source port 16, destination port 16, sequence number 32, acknowledgment number 32, data offset 4
(header length in words), reserved, flags, window 16, checksum 16, urgent pointer 16, options.

Flags: **CWR ECE URG ACK PSH RST SYN FIN** (the RFC 9293 list of currently assigned control bits).

## Options worth knowing (only in SYN where noted)
- MSS (kind 2, SYN only; kinds and RFCs match the IANA TCP option registry): what the receiver can take; clamping devices rewrite it.
- Window scale (kind 3, SYN only, RFC 7323): shift count; real window = window field << scale.
- SACK permitted (kind 4, SYN) and SACK blocks (kind 5).
- Timestamps (kind 8): RTT measurement and PAWS.

## Reading connections
| Pattern | Meaning |
|---|---|
| SYN, no reply, retransmitted with doubling gaps (Linux: initial RTO 1 s, `tcp_syn_retries` 6, giving up after about 131 s; other OSes use other timers) | silently dropped (firewall, routing, host down) |
| SYN -> RST,ACK | host reachable, port closed (or a firewall rejecting with RST) |
| SYN -> SYN,ACK -> ACK, then RST from client | client app aborted or local policy |
| RST arriving with an unexpected TTL | injected by a middlebox (IPS, firewall), not the server |
| FIN from one side, data still from the other | half-close, normal |
| Zero window advertised repeatedly | receiver app not reading; not a network fault |
| Dup ACKs + retransmissions | loss on the path |

Compare TTL and IP ID of a RST with earlier packets from the same server; a mismatch identifies
an injecting device. Capture on both sides to tell which hop altered or dropped packets.

## Wireshark filters
`tcp.flags.syn == 1 && tcp.flags.ack == 0`, `tcp.flags.reset == 1`,
`tcp.analysis.retransmission`, `tcp.analysis.zero_window`, `tcp.options.mss_val`.
Disable "relative sequence numbers" (Wireshark preference `tcp.relative_sequence_numbers`, e.g. `-o tcp.relative_sequence_numbers:FALSE`, accepted by tshark) when comparing captures from two points through a firewall
that randomises ISNs.

## Verify
- [ ] For a failing connection you can state which packet was last seen, from whom, and whether the RST/timeout originates at the endpoint or a middlebox.
