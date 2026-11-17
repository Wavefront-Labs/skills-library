---
id: computing-software.systems-network-administration.wireshark.io-graphs-and-flow-graph
name: io-graphs-and-flow-graph
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wireshark-statistics, io-graph, flow-graph, sequence-diagram, throughput-graph, sum-calc, max-calc, microbursts, tcp-analysis-flags-graph, interval, ladder-diagram]
level: practitioner
status: verified
description: "Use I/O Graphs to correlate throughput with errors (SUM/MAX/COUNT on fields, 1 ms intervals for microbursts) and Flow Graph ladder diagrams for multi-host exchanges."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatIOGraphs.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatFlowGraph.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# I/O Graphs and Flow Graph

## I/O Graphs (Statistics > I/O Graphs)
Each graph line = display filter + Y field + calculation + style.
| Line | Filter | Y axis |
|---|---|---|
| Throughput | (none) | Bits/s, interval 100 ms |
| Problems | `tcp.analysis.flags && !tcp.analysis.window_update` | Packets, red bars |
| Bytes in flight | `tcp.stream eq 3` | `MAX(tcp.analysis.bytes_in_flight)` |
| Server response time | `http.time` | `MAX(http.time)` or `AVG(http.time)` |
| Window | `tcp.srcport==443` | `MIN(tcp.window_size)` |
Calculations: COUNT FRAMES, COUNT FIELDS, SUM, MIN, MAX, AVG, LOAD.

Techniques:
- **Interval matters**: 1 s smooths away microbursts. Drop to 10 ms or 1 ms to see bursts that
  fill switch buffers and cause drops while 1-second averages look idle.
- Click a point on the graph to jump to that packet.
- Log scale Y for mixed small/large series; "Time of day" for correlating with logs.
- Save graphs as PNG/CSV (Save As) for reports; CLI equivalent
  `tshark -r cap.pcapng -q -z io,stat,0.1,"COUNT(tcp.analysis.retransmission)tcp.analysis.retransmission"`.
  In tshark, fields computed by TCP analysis (`tcp.analysis.bytes_in_flight`, `tcp.window_size`) read 0 unless the
  filter part also mentions the field: `"MAX(tcp.analysis.bytes_in_flight)tcp.analysis.bytes_in_flight"` gave 3041 where
  `...tcp.stream eq 0` gave 0 in 4.4.1. `-z flow,tcp,network` prints a text flow graph.

Pattern reading: throughput drops in step with retransmission spikes = loss-driven slowdowns;
throughput plateau at a round number = shaping/policing; zero-window spikes before stalls =
receiver bottleneck.

## Flow Graph (Statistics > Flow Graph)
Ladder diagram of packets between hosts with time and comment (flags, info).
- Tick "Limit to display filter" and set a filter first (one transaction across several hosts:
  client, load balancer, app, DB) to make it readable.
- Flow type: All flows, TCP flows (shows seq/ack), ICMP, etc. Address type: network or any.
- Export as PNG/PDF/ASCII for tickets; ideal for explaining a DHCP DORA, a TCP handshake failing
  at a firewall, or a SIP call (VoIP Calls uses the same view).

## Verify
- [ ] I/O graph with problems line explains the user's "slow at 10:05" with a visible event.
- [ ] Flow graph of the filtered transaction shows each hop in order with timings.

## Checked
Run on Wireshark 4.4.1: the tshark `io,stat` command with a `COUNT(...)` column ran, MAX, MIN, AVG, SUM, LOAD and COUNT columns
all produced values, and the 0-versus-3041 behaviour of analysis fields was measured on a synthetic capture; `-z flow,tcp,network`
printed a ladder. The calculation names (SUM, COUNT FRAMES, COUNT FIELDS, MAX, MIN, AVG, LOAD), Save As image or CSV, click
to jump to the packet, "Time of day", "Limit to display filter", flow-type and address options, and PNG/PDF/ASCII flow-graph
export come from the Wireshark User's Guide I/O Graphs and Flow Graph pages. The pattern-reading paragraph is practitioner
guidance.
