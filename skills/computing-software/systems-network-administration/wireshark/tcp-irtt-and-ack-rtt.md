---
id: computing-software.systems-network-administration.wireshark.tcp-irtt-and-ack-rtt
name: tcp-irtt-and-ack-rtt
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcp-analysis, irtt, ack-rtt, round-trip-time, latency, capture-point]
level: practitioner
status: verified
description: "Measure network round-trip time from a capture using tcp.analysis.initial_rtt and ack_rtt, account for capture position, and separate path latency from host delay."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html
  - https://www.wireshark.org/docs/dfref/t/tcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iRTT and ACK RTT

## Initial RTT (iRTT)
`tcp.analysis.initial_rtt` = time from SYN to the ACK that completes the handshake, as seen at the
capture point (test: SYN at t0, ACK at t0+0.040 gave 0.040000). Shown under SEQ/ACK analysis on every packet of the stream.
```
tcp.analysis.initial_rtt > 0.1
```
Add it as a column, then Statistics > Conversations > TCP sorted by stream to compare clients.

## Where you capture changes the meaning
- Capture on the client: iRTT ~ SYN to SYN/ACK = full network RTT to the server (plus server
  kernel time, tiny).
- Capture on the server: iRTT ~ SYN/ACK to ACK = full RTT to the client.
- Capture in the middle: SYN->SYN/ACK = RTT to server side; SYN/ACK->ACK = RTT to client side.
  Their sum is the end-to-end RTT; Wireshark reports the total.

## ACK RTT
`tcp.analysis.ack_rtt` = time between a data segment and the ACK that covers it. Inflated by:
delayed ACKs (RFC 9293 requires the delay to be under 0.5 s), receiver application
not reading, or queueing. Use it as a distribution, not a single number.
```
tcp.analysis.ack_rtt > 0.2
```
IO Graph with `AVG(*)tcp.analysis.ack_rtt` over time shows queue build-up (bufferbloat) during
transfers.

## Separate network from server time
- Network: iRTT (handshake handled by kernel, no app involved).
- Server: time from request (`http.request`) to first response byte minus iRTT. HTTP gives
  `http.time`; for other protocols use `tcp.time_delta` with conversation timestamps on.
If `http.time` is 900 ms and iRTT is 20 ms, the server took ~880 ms: not a network problem.

## Gotchas
- Retransmitted SYNs make iRTT include the retry wait (1 s, 3 s): filter
  `tcp.flags.syn==1 && tcp.analysis.retransmission` first.
- SYN cookies, load balancers and proxies terminate TCP; iRTT then measures to the proxy.
- Capture timestamp precision limits how small an RTT you can trust (see timestamp accuracy).

## Verify
- [ ] iRTT values match `ping`/`mtr` RTT to the same endpoint within a few ms.
