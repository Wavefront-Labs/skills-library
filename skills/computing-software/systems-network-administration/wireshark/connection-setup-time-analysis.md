---
id: computing-software.systems-network-administration.wireshark.connection-setup-time-analysis
name: connection-setup-time-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, connection-setup-time, tcp-handshake, tls-handshake, dns-time, performance-analysis]
level: practitioner
status: verified
description: "Break down connection setup time in captures: DNS lookup, TCP handshake, TLS handshake and first byte, and find which phase delays the user."
sources:
  - https://www.wireshark.org/docs/dfref/t/tcp.html
  - https://www.wireshark.org/docs/dfref/t/tls.html
  - https://www.rfc-editor.org/rfc/rfc8446
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection setup time

Time to first byte = DNS + TCP handshake + TLS handshake + request + server processing.

## Measure each phase (client-side capture)
| Phase | How |
|-------|-----|
| DNS | `dns.time` on the response for the hostname |
| TCP | SYN to SYN/ACK: `tcp.analysis.ack_rtt` on the SYN/ACK (if the SYN was retransmitted it is measured from the first SYN). `tcp.analysis.initial_rtt` is SYN to the client's final handshake ACK, shown from that ACK onward |
| TLS | ClientHello to Finished; TLS 1.3 = 1 RTT, TLS 1.2 = 2 RTT, plus certificate size effects |
| Request to first response byte | `http.time` or first data packet after request |

Filters:
```
tcp.flags.syn == 1 && tcp.flags.ack == 0
tcp.analysis.retransmission && tcp.flags.syn == 1      # SYN retries: 1 s, 3 s delays
tls.handshake.type == 1 || tls.handshake.type == 2 || tls.handshake.type == 20
```

## Typical delays and causes
| Observation | Cause |
|-------------|-------|
| DNS 5 s then success | first resolver timed out, second answered; or AAAA timeout |
| SYN retransmitted after 1 s / 3 s | SYN dropped: firewall, SYN backlog, ECMP asymmetry |
| Long gap between ClientHello and ServerHello | server CPU (RSA), TLS offload overloaded, SNI routing |
| Big certificate chain over several RTTs | initial congestion window limit; trim chain |
| Client waits after ServerHelloDone | client cert revocation checks (OCSP/CRL) |
| Happy Eyeballs: IPv6 SYN with no answer, IPv4 attempt about 250 ms later (RFC 8305's recommended Connection Attempt Delay) | broken IPv6 path |

## tshark summary per stream
```
tshark -r in.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==1" -T fields -e tcp.stream -e ip.src -e tcp.analysis.ack_rtt
```

## Verify
- [ ] The sum of phases matches the browser dev tools timing (DNS, Connect, SSL, TTFB).

## Checked
Run on Wireshark 4.4.1 with synthetic captures: a SYN retransmitted at 1 s and 3 s matched
`tcp.analysis.retransmission && tcp.flags.syn == 1` and the SYN/ACK's `tcp.analysis.ack_rtt` was 3.05 s (from the first
SYN); in a clean handshake with a 30 ms SYN to SYN/ACK gap, `ack_rtt` on the SYN/ACK was 0.030 s while `initial_rtt` was
0.031 s (SYN to final ACK) and appeared from the third packet on; the TLS handshake-type filter (1, 2, 20 = Finished)
matched; the per-stream tshark command printed the stream, server and RTT. RFC 6298 gives the 1 s initial RTO that
explains the 1 s and 3 s retry times, RFC 8305 the 250 ms attempt delay, the flight diagrams in RFC 5246 (figure 1) and RFC 8446 (section 2) give 2 and 1 round trips for TLS 1.2 and 1.3. DNS
`dns.time` was measured on answered queries. The list of causes is practitioner guidance.
