---
id: computing-software.systems-network-administration.wireshark.tcp-analysis-flags-filter-library
name: tcp-analysis-flags-filter-library
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, display-filter, tcp-analysis-flags, expert-info, troubleshooting-filters, filter-buttons]
level: practitioner
status: verified
description: "A practical display filter library for troubleshooting: tcp.analysis flags, expert severity, slow responses, handshake failures and errors across DNS/HTTP/TLS, saved as buttons."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html
  - https://www.wireshark.org/docs/dfref/t/tcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting filter library

## TCP health
```
tcp.analysis.flags && !tcp.analysis.window_update     # all TCP problems, minus noise
tcp.analysis.retransmission || tcp.analysis.fast_retransmission
tcp.analysis.lost_segment                              # gap seen: loss before capture point
tcp.analysis.duplicate_ack_num >= 3
tcp.analysis.zero_window || tcp.analysis.window_full
tcp.analysis.ack_rtt > 0.2                             # slow ACKs
tcp.time_delta > 1 && tcp.len > 0                      # stalls inside a stream
```
`tcp.time_delta` needs the TCP preference "Calculate conversation timestamps" (`tcp.calculate_timestamps`, TRUE by default in 4.4.1
per `tshark -G defaultprefs`; enable it on older versions). All filters on this page were accepted by TShark 4.4.1.

## Connection setup
```
tcp.flags.syn == 1 && tcp.flags.ack == 0               # SYNs
tcp.flags.syn == 1 && tcp.analysis.retransmission      # SYN retries: no answer/filtered
tcp.flags.reset == 1                                   # resets
tcp.completeness < 7                                   # frames seen before the 3-way handshake completed (3.6+)
```

`tcp.completeness` is cumulative per stream: in a test stream the packets carried 0, 1, 3, 7, 15, 15, 31 as SYN, SYN-ACK, ACK, data and
FIN/RST were seen (`tcp.completeness.str` renders it as flags such as `···ASS`; the per-flag sub-fields are 4.2+). So `< 7` means "handshake not
yet complete as of this packet", not "stream never completed". Use `tcp.completeness == 31` or the `.syn`/`.fin` sub-fields for finished streams.

## Expert info
```
_ws.expert.severity >= warning
_ws.expert.group == "Malformed"
```

## Application errors and latency
```
dns.flags.rcode != 0                     # NXDOMAIN, SERVFAIL, REFUSED
dns.time > 0.5
http.response.code >= 400
http.time > 1
tls.alert_message
tls.handshake.type == 1                  # Client Hello (SNI in tls.handshake.extensions_server_name)
icmp.type == 3 || icmpv6.type == 1       # destination unreachable
kerberos.error_code
smb2.nt_status != 0
```

## Save as buttons
Display filter buttons are stored in the `dfilter_buttons` file of the configuration profile (User's Guide, Files and Folders), so build a
Troubleshooting profile and share that file with the team. Saved filters (Analyze > Display Filters) are kept in `dfilters`.

## Gotchas
- Expert flags depend on what the capture saw; a capture with drops shows false "previous segment
  not captured" and "ACKed unseen segment".
- Use `tcp.stream eq N` after finding a bad packet to isolate the conversation before drawing
  conclusions.

## Verify
- [ ] The profile directory contains the shared `dfilter_buttons` and each filter returns plausible packets on a known-bad capture.
