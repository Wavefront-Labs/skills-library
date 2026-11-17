---
id: computing-software.systems-network-administration.wireshark.network-vs-application-delay
name: network-vs-application-delay
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, latency-analysis, performance-analysis, application-delay, server-response-time, network-latency, initial-rtt, tcp-analysis-ack-rtt, think-time, it-s-the-network, http-time, time-reference]
level: practitioner
status: verified
description: "Prove whether slowness is network, server or client from a capture: handshake RTT, ACK vs response timing, server and client think time, transfer time."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html
  - https://www.wireshark.org/docs/dfref/t/tcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network vs application delay

Break one slow transaction into its parts. Capture as close to the **client** as possible
(sees what the user experiences), ideally also at the server.

## 1. Network round trip
- `tcp.analysis.ack_rtt` on the SYN/ACK = SYN to SYN/ACK, the path RTT baseline from a client capture.
  `tcp.analysis.initial_rtt` is SYN to the client's final handshake ACK (RTT plus client turnaround) and is shown
  on every packet of the stream from that ACK onward.
- `tcp.analysis.ack_rtt` on server ACKs: how fast the stack acknowledged data.

## 2. Server think time (application delay)
Request sent -> server **ACKs** quickly (~1 RTT) -> long gap -> response data.
- Fast ACK + slow data = server application/backend is slow (database, auth, disk). Not the network.
- For HTTP: `http.time` on the response (request to the frame where the response is dissected; for a response
  reassembled from several segments that is the LAST segment, so it includes transfer time: 1.252 s in the test where
  the first response byte came after 1.250 s). DNS: `dns.time`.
  SMB2: `smb2.time`. Generic: Statistics > Service Response Time.
- Column `tcp.time_delta` (conversation timestamps; on by default in 4.4.1) shows the gap since the previous packet of the stream, so on the first response packet it is the gap after the server's ACK.

## 3. Transfer time (network capacity / TCP behaviour)
First response byte to last byte. Long because of: large size over a high-RTT path (window
limited: check `tcp.analysis.bytes_in_flight` vs window), packet loss (retransmissions), receiver
zero windows, shaping. See the TCP analysis skills.

## 4. Client think time
Gap between receiving a response and sending the next request (`tcp.time_delta` on the client's
next request). Chatty applications doing hundreds of sequential small requests suffer from RTT
x number of turns, not bandwidth: 200 turns x 40 ms RTT = 8 s regardless of link speed.

## Summary table to report
| Component | Measured | Evidence (packet numbers) |
|---|---|---|
| RTT | 38 ms | 1-3 |
| Server think | 2.4 s | 12 -> 13 |
| Transfer | 0.3 s | 13 -> 58 |
| Client think | 0.1 s | 58 -> 60 |

## Gotchas
- Capture on the server only: you will not see network delay in front of it (proxies, WAN).
- Load balancers/proxies terminate TCP: there are two connections; capture both sides.
- TLS: handshake adds 1-2 RTT before the request; count it in the network/latency budget.

## Verify
- [ ] Each component timed with packet references from one representative transaction.
- [ ] Conclusion matches a second transaction (not a one-off).

## Checked
Run on Wireshark 4.4.1 against a synthetic client-side capture (SYN to SYN/ACK 30 ms, request at 1.000, ACK at 1.031, response
from 2.250 in three segments, next request 0.1 s after the last ACK): `ack_rtt` 0.030 on the SYN/ACK, `initial_rtt` 0.031
from frame 3 on, `tcp.time_delta` 1.219 on the first response segment (gap after the ACK), `http.time` 1.252 on the last
response segment, `tcp.analysis.bytes_in_flight` 3041 at the end, and `tcp.time_delta` 0.100 on the next request. The
field names `smb2.time` and `dns.time` exist. The worked numbers in the table are illustrative.
