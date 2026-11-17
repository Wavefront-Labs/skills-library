---
id: computing-software.systems-network-administration.cisco-networking.span-oversubscription-and-drops
name: span-oversubscription-and-drops
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, span, span-oversubscription, port-mirroring, network-tap, packet-drops, monitor-session]
level: practitioner
status: draft
description: "Recognise when SPAN copies are being dropped (oversubscribed destination, both-direction sources, platform priority) and when to use a TAP or packet broker instead."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/nmgmt/b_179_nmgmt_9300_cg/configuring_span_and_rspan.html
  - https://wiki.wireshark.org/CaptureSetup/Ethernet
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SPAN oversubscription and drops

SPAN is best-effort: the switch delivers production traffic first and silently discards
mirror copies it cannot fit. A capture with gaps from SPAN looks exactly like a network
problem (missing segments, "ACKed unseen segment", phantom retransmissions).

## Arithmetic
A 1 Gb full-duplex source mirrored `both` can produce up to 2 Gb/s of copies. Into a 1 Gb
destination that is guaranteed loss at load. Sources aggregated from several ports or a VLAN
multiply it.

## Detect drops
- Switch: `show interfaces Gi1/0/48` output drops on the destination; on Catalyst 9000
  `show platform hardware fed switch active qos queue stats interface Gi1/0/48`.
- Capture: Wireshark `tcp.analysis.ack_lost_segment` ("ACKed segment that wasn't captured")
  appearing in bursts is the signature of capture loss, not network loss.
- Capture host: `dumpcap` / `tshark` summary "packets dropped" (host-side, different cause).

## Mitigate
1. Mirror only one direction or filter by VLAN/ACL (`monitor session 1 filter ...`,
   FSPAN ACL on platforms that support it).
2. Use a destination port faster than the sum of sources.
3. Capture nearer the host (one access port) instead of an aggregated VLAN.
4. Use a **TAP** for evidence-grade or high-rate captures: passive, copies every frame
   including errors, no CPU/priority issues. An aggregating TAP has its own oversubscription.
5. Packet brokers for permanent monitoring fabrics.

## Also missing in SPAN copies
Frames with CRC errors, runts and some control frames are not mirrored; hardware errors are
invisible through SPAN.

## Verify
- [ ] Destination output drops stay at zero during the capture window, and no bursts of
      "ACKed unseen segment" without matching retransmissions.
