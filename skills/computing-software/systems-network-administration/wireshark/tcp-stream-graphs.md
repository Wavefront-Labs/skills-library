---
id: computing-software.systems-network-administration.wireshark.tcp-stream-graphs
name: tcp-stream-graphs
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcp-stream-graph, tcptrace, stevens-graph, throughput-graph, rtt-graph, window-scaling-graph, tcp-analysis]
level: practitioner
status: verified
description: "Read Wireshark TCP stream graphs (Stevens, tcptrace, throughput, RTT, window scaling) to tell sender, receiver and network limits apart on a slow transfer."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatTCPStreamGraphs.html
  - https://wiki.wireshark.org/TCP_Analyze_Sequence_Numbers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP stream graphs

Select a packet of the data-carrying direction (the server sending the download), then
Statistics > TCP Stream Graphs. Graphing the wrong direction gives a flat, useless plot; use
"Switch Direction" (the label is in the 4.4.1 binary).
The 4.4.1 menu offers: Time Sequence (Stevens), Time Sequence (tcptrace), Throughput, Round Trip Time and Window Scaling.

## tcptrace (the most informative)
Shows forward segments, acknowledgements, selective acknowledgements, reverse window sizes and zero windows (User's
Guide). Y = sequence number, X = time.
- Segments rising smoothly = steady transfer; slope = throughput. Series colours are not documented in the guide, so
  read the legend in your build.
- Segments hitting the window line repeatedly = **receiver window limited** (small rwnd,
  no window scaling): fix the receiver/app or scaling.
- Gaps and re-sent segments lower than the leading edge = **retransmissions** (loss); selective acknowledgements are drawn
  too (the guide lists them among the tcptrace series).
- Flat steps (send, pause, send) well below the window = **sender limited** (the sender, not the receiver or network, is
  the bottleneck).

## Stevens
Stevens: "a simple graph of the TCP sequence number over time" (User's Guide); quick visual of stalls and slope changes.

## Throughput
Average throughput and goodput (User's Guide): compare against link capacity and the
bandwidth-delay product (throughput <= window / RTT).

## Round Trip Time
RTT versus time or sequence number, based on the acknowledgment timestamp for each segment (User's Guide). Read it next to the Throughput graph.

## Window Scaling
Window size and outstanding bytes (User's Guide). Window near 0 = zero-window events (receiver app
not reading).

## Gotchas
- Window scaling needs the SYN in the capture; without it Wireshark cannot know the scale
  factor and windows look tiny ("window size scaling factor: -1 (unknown)").

## Verify
- [ ] Diagnosis names one limit (receiver window, sender/app, network loss/latency) with the graph that shows it.

## Checked
Graph menu names and what each graph plots were read from the 4.4.1 User's Guide shipped with the install (Statistics,
TCP Stream Graphs). The Wireshark message `Window size scaling factor: -1 (unknown)` was reproduced in TShark 4.4.1 on a
capture with no SYN (also shows `Calculated window size: 8192` for a 8192 window). The graphs are GUI-only, so the
interpretation advice was reduced to what the guide documents.
