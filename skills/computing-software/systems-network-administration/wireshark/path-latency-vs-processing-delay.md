---
id: computing-software.systems-network-administration.wireshark.path-latency-vs-processing-delay
name: path-latency-vs-processing-delay
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, path-latency, processing-delay, rtt, performance-analysis]
level: practitioner
status: verified
description: "Separate network path latency from server and client processing delay in captures using handshake RTT, ACK timing and request-to-response gaps."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html
  - https://www.wireshark.org/docs/dfref/t/tcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path latency vs processing delay

The core question in "the network is slow": is time spent on the wire, or in an endpoint?

## Measure path latency
- TCP handshake: on the client, SYN to SYN/ACK delta = network RTT (servers answer SYNs in the
  kernel, almost no processing). Field `tcp.analysis.ack_rtt` on the SYN/ACK gives SYN to SYN/ACK; `tcp.analysis.initial_rtt` (SYN to the final handshake ACK) is shown on every packet of the stream from that ACK onward.
- Pure ACK timing: data segment to its ACK (`tcp.analysis.ack_rtt`), but beware delayed ACK (RFC 9293 requires it to be under 0.5 s; stacks commonly use tens to a couple of hundred ms).
- ICMP echo as a sanity check.

## Measure processing delay
Request sent, then the server's TCP ACK arrives quickly (RTT), then the response data arrives much
later: the gap after the ACK is server processing.
```
http.time                                      # on the response frame; last segment if the response was reassembled
dns.time
smb2.time
tcp.time_delta > 0.2 && tcp.len > 0           # needs "calculate conversation timestamps" (on by default in 4.4.1)
```
Server-side capture is best: request arrival to response departure is pure server time.

## Worked example
Initial RTT 30 ms; HTTP request at t=0.000, ACK at t=0.031, first response byte at t=1.250.
Network ~30 ms, server ~1.2 s. Network team can stop.

## Client delay
Response fully received, next request only after a long gap: client think time or client
processing (rendering, local DB), not network.

## Gotchas
- Capturing in the middle of the path shows partial RTTs; add both halves (client side + server side).
- Proxies and load balancers terminate TCP; the handshake RTT is to the proxy, not the server.

## Verify
- [ ] Sum of measured network RTTs and processing gaps explains the user-observed response time.

## Checked
Run on Wireshark 4.4.1 against a synthetic capture with a 30 ms handshake RTT, an ACK 31 ms after the request and the
first response byte 1.250 s after the request: the measured values were `ack_rtt` 0.030, ACK after the request 0.031 s,
`tcp.time_delta` 1.219 s on the first response packet, and `tcp.time_delta > 0.2 && tcp.len > 0` matched the response and
the next request; the worked example in the skill is the same arithmetic. The delayed-ACK bound is RFC 9293 (MUST be
under 0.5 s); the field names `smb2.time` and `dns.time` exist.
