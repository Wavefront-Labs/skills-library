---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.wireshark-expert-info-and-anomaly-spotting
name: wireshark-expert-info-and-anomaly-spotting
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [expert-info, wireshark, tcp-analysis, retransmissions, anomalies, pcap-triage, dfir]
level: practitioner
status: verified
description: "Use Wireshark Expert Information and TCP analysis flags to spot malformed packets, retransmission storms, resets and protocol anomalies that mark malicious traffic."
sources: ["https://www.wireshark.org/docs/wsug_html_chunked/ChAdvExpert.html", "https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expert info and anomaly spotting

**Goal:** let Wireshark's dissectors point out what is unusual in a capture, then decide which
anomalies are network problems and which are attacker behaviour.

## Open it
Analyze > Expert Info (or click the expert level indicator in the status bar).
Entries are grouped by severity: **Error** (malformed, bad checksum when checksum validation is on; it is off by default for TCP in 4.4.1),
**Warning** (unusual: resets, zero window, previous segment not captured), **Note**
(retransmissions, duplicate ACKs), **Chat** (normal workflow: SYN, FIN, HTTP requests).
Display-filter them: `_ws.expert`, `_ws.expert.severity == error`, `_ws.malformed`.

## Useful TCP analysis filters
```
tcp.analysis.flags && !tcp.analysis.window_update
tcp.analysis.retransmission || tcp.analysis.fast_retransmission
tcp.flags.reset == 1
tcp.analysis.zero_window
tcp.analysis.lost_segment          # "previous segment not captured": capture gap
tcp.flags.syn == 1 && tcp.flags.ack == 0    # connection attempts (scan detection)
```

## Reading anomalies forensically
| Observation | Possible meaning |
|---|---|
| Many SYNs, few SYN/ACKs, RSTs back | port scan or failed C2 to sinkholed/blocked hosts |
| Malformed packets on a standard port | non-standard protocol tunnelled over 443/53/80, or exploit traffic |
| Long DNS labels, many TXT queries (Wireshark raises no expert item for these: none appeared in a test, so filter on `dns.qry.name.len` and `dns.qry.type`) | DNS tunnelling |
| TLS alerts (`tls.alert_message`; not an expert item either), handshake failures to one IP | C2 with bad certs, interception, or blocked egress |
| `lost_segment` across the capture | the capture dropped packets: content reconstruction will have gaps; note in report |
| Retransmission bursts to one external IP during large uploads | possible exfiltration over congested link |
| Checksum errors on all outbound packets | checksum offload artefact (disable validation: harmless) |

## Workflow
1. Open Expert Information, sort by count, read Errors and Warnings first.
2. Right-click an entry > Apply as Filter to see packets; follow the stream.
3. Combine with Statistics > Conversations/Endpoints to see whether anomalies cluster on one
   host pair.

## Gotchas
- Expert info depends on dissectors recognising the protocol; Decode As the right protocol for
  non-standard ports first.
- Capture-side issues (SPAN drops, offload) generate noise; check capture method before
  treating gaps as evidence.

## Self-check
Every anomaly you report is classified as capture artefact, network fault or suspicious, with
the filter you used to isolate it.

## Checked
Run on Wireshark 4.4.1 with captures covering retransmissions, duplicate ACKs, keep-alives, zero windows, RSTs, gaps, a
malformed EAP frame, a bad TCP checksum, long DNS names and a TLS alert: `-z expert` listed the items under the severities
stated (Warns: zero window, RST, previous segment not captured; Notes: retransmissions, duplicate ACKs; Chats: SYN and
FIN), every filter in the TCP block and `_ws.expert`, `_ws.expert.severity`, `_ws.malformed` matched, the bad checksum
became an Error only with `-o tcp.check_checksum:TRUE`, and DNS tunnelling traits and the TLS alert raised no expert item.
The dialog name and status-bar indicator are from the Wireshark User's Guide expert-information chapter.
