---
id: computing-software.systems-network-administration.wireshark.previous-segment-not-captured-and-acked-unseen
name: previous-segment-not-captured-and-acked-unseen
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcp-analysis, previous-segment-not-captured, acked-unseen-segment, capture-drops, packet-loss, expert-info]
level: practitioner
status: verified
description: "Tell real network loss from capture loss: what Previous segment not captured and ACKed unseen segment mean, capture-point effects, and how to confirm with drop counters."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Previous segment not captured vs ACKed unseen segment

## Definitions
- `[TCP Previous segment not captured]`: a segment's sequence number is higher than the next
  expected; bytes in between were not seen by the capture.
- `[TCP ACKed unseen segment]`: an ACK acknowledges data the capture never saw.

## Decision table
| Seen | Interpretation |
|---|---|
| Previous segment not captured, followed by dup ACKs and a retransmission | real loss upstream of the capture point (the receiver also missed it) |
| Previous segment not captured, no dup ACKs, the receiver ACKs past the gap | the receiver got it; the capture missed it (capture drop or SPAN oversubscription) |
| ACKed unseen segment | capture missed it, almost always (the receiver obviously had it) |
| Both at the very start of a stream | capture started mid-connection; harmless |

So "ACKed unseen" points at your capture, not the network.

## Confirm capture drops
```
capinfos cap.pcapng                        # prints "Packets received/dropped on interface ..." (pcapng only)
```
Status bar in Wireshark shows `Dropped: N` after a live capture. Also check the SPAN/mirror session: the destination port's output drop counters (see your switch
vendor's docs); mirroring a faster uplink to a slower port loses packets under load.

## Where the capture sits matters
Capturing on the sender host: packets lost in the network appear as normal sends followed by
retransmissions (no "not captured" marker, because the sender saw them). Capturing on the receiver:
lost packets show as "previous segment not captured" with dup ACKs. Comparing two capture points
localises the loss (see dual captures).

## Filters
(Run on a synthetic capture in Wireshark 4.4.1: a gap followed by a later segment gave `lost_segment`; an ACK past the
highest sequence ever seen gave `ack_lost_segment`; an ACK for data after a gap that had later segments seen did not.)
```
tcp.analysis.lost_segment
tcp.analysis.ack_lost_segment
tcp.analysis.lost_segment || tcp.analysis.ack_lost_segment
```

## Gotchas
- Segmentation/receive offload on host captures merges segments; Wireshark may still mark gaps oddly.
  Disable the offloads on the capturing NIC (OS and driver specific) when analysing on a host.
- Out-of-order delivery shows a gap followed by the missing segment arriving late, marked
  `Out-Of-Order`, not loss.

## Verify
- [ ] Before reporting network loss, show dup ACKs plus a retransmission for the same sequence and
  zero capture drops.
