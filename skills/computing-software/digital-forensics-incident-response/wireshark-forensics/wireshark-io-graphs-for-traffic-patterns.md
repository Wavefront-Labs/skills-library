---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.wireshark-io-graphs-for-traffic-patterns
name: wireshark-io-graphs-for-traffic-patterns
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [io-graph, wireshark, traffic-patterns, beaconing, exfiltration, dfir]
level: practitioner
status: gated
description: "Use Wireshark I/O Graphs to spot beaconing, exfil bursts and scans: graph items with display filters, intervals, SUM/COUNT of fields, and tshark -z io,stat for repeatable numbers."
sources: ["https://www.wireshark.org/docs/wsug_html_chunked/ChStatIOGraphs.html", "https://www.wireshark.org/docs/man-pages/tshark.html", "https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wireshark I/O graphs for traffic patterns

Statistics > I/O Graphs plots packets, bytes or field values over time for any display filter. Patterns hard to see in a packet list (regular check-ins, a 20-minute upload, a scan) are obvious on a graph.

## Building graphs
Each row in the graph table is an item: name, display filter, colour, style (line, bar, dot), Y axis unit (packets, bytes, bits, or `SUM(Y Field)`, `COUNT FRAMES(Y Field)`, `MAX`, `AVG`, `LOAD`), Y field, and smoothing. Set the interval (1 ms to 10 min) at the bottom and switch to time of day for correlation with logs.

## Useful items
| Question | Filter / Y axis |
|---|---|
| Is a host beaconing? | `ip.addr==10.1.2.3 && tcp.flags.syn==1 && tcp.flags.ack==0`, packets, interval 10 s; regular spikes = beacon |
| Upload burst (exfiltration)? | `ip.src==10.1.2.3 && !(ip.dst==10.0.0.0/8)`, `SUM(Y Field)` with `tcp.len` or bytes; compare with download item |
| DNS tunnelling volume | `dns.qry.name contains "example-c2.com"`, packets, 1 min |
| Retransmissions / network trouble | `tcp.analysis.retransmission`, packets |
| Scan | `tcp.flags.syn==1 && tcp.flags.ack==0`, packets, 1 s; vertical wall = scan |
| Request rate per web path | `http.request.uri contains "/upload"`, packets |
Click a point on the graph to jump to the first packet in that interval.

## Reproducible numbers with tshark
```bash
tshark -r cap.pcapng -q -z io,stat,60,"ip.src==10.1.2.3","SUM(tcp.len)tcp.len && ip.src==10.1.2.3"
tshark -r cap.pcapng -q -z io,stat,10,"tcp.flags.syn==1 && tcp.flags.ack==0"
```
Output tables per interval go straight into the report or a spreadsheet; the GUI graph is for exploration.

## Tips
- Use log scale when one item dwarfs others.
- Save graph configurations in an investigation profile so the team reuses them.
- Copy (button) exports the data points as CSV for exhibits.

## Gotchas
- Interval choice hides or reveals patterns: jittered beacons need intervals near the beacon period; try several.
- `SUM` on fields that appear multiple times per frame double-counts; check the field occurrence.
- Captures with gaps (ring buffers, dropped packets) look like quiet periods; check capinfos and drop counts.

## Verify
Pattern claims (e.g. "beacon every 60 s") are backed by a tshark io,stat table or exported data points, not only a screenshot.

## Checked

- Date: 2026-11-02.
- Confirmed against: I/O Graph Y-axis functions SUM(Y Field) and COUNT FRAMES(Y Field) (Wireshark User Guide ChStatIOGraphs); display filter ip.src== and tcp.flags.syn boolean field semantics (display filter docs).
- Not confirmed: the combined SUM(tcp.len) and ACK/SYN filter strings and beaconing interpretation (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
