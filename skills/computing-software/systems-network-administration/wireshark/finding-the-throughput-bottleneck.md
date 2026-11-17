---
id: computing-software.systems-network-administration.wireshark.finding-the-throughput-bottleneck
name: finding-the-throughput-bottleneck
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, throughput-bottleneck, bytes-in-flight, receive-window, bandwidth-delay-product, tcp-analysis, performance-analysis]
level: practitioner
status: verified
description: "Work out why a TCP transfer is slow: receiver window, sender or app limit, congestion and loss, or path capacity, using bytes in flight and stream graphs."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatTCPStreamGraphs.html
  - https://www.rfc-editor.org/rfc/rfc7323
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding the throughput bottleneck

Throughput <= window / RTT. A transfer is limited by one of: the receiver's advertised window, the
sender's congestion window (loss), the sending application, or the path's capacity.

## Gather three numbers
1. RTT: `tcp.analysis.initial_rtt` for the stream (SYN to the client's final handshake ACK, shown from that packet on; `ack_rtt` on the SYN/ACK is SYN to SYN/ACK).
2. Bytes in flight: add `tcp.analysis.bytes_in_flight` as a column (data side packets).
3. Receiver window: `tcp.window_size` (calculated, after scaling) on ACKs from the receiver.
   In `tshark -z io,stat` these two fields read 0 unless the filter also mentions them, e.g.
   `"MAX(tcp.analysis.bytes_in_flight)tcp.stream eq 0 && tcp.analysis.bytes_in_flight"`.

## Diagnose
| Observation | Bottleneck |
|---|---|
| bytes_in_flight hits the receiver window repeatedly, `[TCP Window Full]` markers | receiver window: small buffer or window scaling stripped. Check SYN for `wscale` on both sides |
| Window large, bytes_in_flight saw-tooths down after retransmissions | congestion control reacting to loss |
| bytes_in_flight low and irregular, gaps with no data while window open | sender application not supplying data (disk, CPU, app design) |
| Smooth, flat throughput at a round number (e.g. 94 Mbit/s) | path capacity or a shaper/policer |
| Receiver sends zero window | receiving application not reading |

Tools: Statistics > TCP Stream Graphs > Window Scaling (bytes in flight vs receive window),
Stevens/tcptrace (slope = throughput, gaps = stalls), Throughput graph.

## Worked numbers
RTT 80 ms, window 64 KB (no scaling) -> max 65535 B / 0.08 s ~ 6.5 Mbit/s whatever the link speed.
That is the classic "fast link, slow transfer over WAN": window scaling missing (a middlebox
stripped the option, or an old stack). Bandwidth-delay product for 1 Gbit/s at 80 ms is 10 MB; the
window must reach that.

## Capture side matters
Measure at the sender for congestion behaviour (what it put in flight); at the receiver for what
arrived. Bytes in flight is only meaningful when the capture sees both data and ACKs.

## Verify
- [ ] Calculated window/RTT matches observed throughput, and the limiting factor is named with
  evidence (graph screenshot or column values).

## Checked
Run on Wireshark 4.4.1 against a synthetic download whose receiver advertised 3000 bytes with 1000-byte segments: bytes in
flight rose 1000, 2000, 3000 per round, `tcp.analysis.window_full` (shown as `[TCP Window Full]`) fired on the segment that
filled the window, the SYN/ACK's `tcp.options.wscale.shift` 7 and multiplier 128 were read, `tcp.window_size` showed the
calculated window, and an unscaled capture reported scale factor -1. The worked numbers were computed: 65535 B / 0.08 s =
6.55 Mbit/s, a 1 Gbit/s x 80 ms bandwidth-delay product is 10 MB, and 1448/1538 gives 94.1 Mbit/s TCP goodput on 100 Mbit
Ethernet (the 'round number' example). The TCP Stream Graphs menu path and graph names (Window Scaling, Stevens, tcptrace,
Throughput, Round Trip Time) are in the User's Guide.
