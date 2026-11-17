---
id: computing-software.systems-network-administration.wireshark.conversations-and-endpoints
name: conversations-and-endpoints
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tshark, wireshark-statistics, protocol-hierarchy, conversations, endpoints, top-talkers, statistics-menu, limit-to-display-filter, tshark-z-conv, capture-triage]
level: practitioner
status: verified
description: "Triage an unfamiliar capture in minutes: Protocol Hierarchy, Conversations and Endpoints windows, top talkers, limiting to display filter, and the tshark -z equivalents."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatConversations.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatEndpoints.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatHierarchy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conversations, endpoints and protocol hierarchy

Before reading packets, get the shape of the capture.

## 1. Statistics > Capture File Properties
Duration, packet count, average rate, **dropped packets** (if the capturing tool recorded
them), interface, snaplen. Dropped packets > 0 means analysis flags may be capture artefacts.

## 2. Statistics > Protocol Hierarchy
Percent of packets and bytes per protocol. Look for surprises: unexpected protocols (SMBv1,
Telnet, LLMNR/NBNS, unknown UDP), "Data" (undissected payload: maybe a non-standard port to
Decode As), or a high share of retransmission-bearing TCP. Right-click > Apply as Filter.

## 3. Statistics > Conversations
Tabs: Ethernet, IPv4, IPv6, TCP, UDP. Columns: addresses, ports, packets, bytes each direction,
Rel Start, Duration, bits/s each direction.
- Sort by Bytes to find top talkers; by Duration for long-lived flows; by Rel Start to see what
  started at the incident time.
- Tick **Limit to display filter** to compute only over what you filtered.
- Right-click a conversation > Apply as Filter > Selected > A<->B; or Follow Stream.
- Enable "Name resolution" in the window only if you need names (see name-resolution-settings).

## 4. Statistics > Endpoints
Per host totals. Good for: who talks to the most peers (scanners), external IPs (add GeoIP
MaxMind databases in Preferences > Name Resolution to get country/ASN columns), MACs on a LAN.

## tshark equivalents
```
tshark -r cap.pcapng -q -z io,phs                    # protocol hierarchy
tshark -r cap.pcapng -q -z conv,tcp                  # TCP conversations
tshark -r cap.pcapng -q -z conv,ip,"ip.addr==10.0.0.0/8"
tshark -r cap.pcapng -q -z endpoints,ip
capinfos cap.pcapng                                  # file properties
```

All five commands ran (`io,phs`, `conv,tcp`, `conv,ip` with a filter, `endpoints,ip`, `capinfos`); `capinfos` also
prints "Packets received/dropped on interface" for pcapng captures made by dumpcap, which is where the dropped-
packet count comes from.

## Reading patterns
- One internal host with conversations to hundreds of external IPs on 443 at regular
  intervals = beaconing candidate (see beaconing-and-dns-tunnelling-detection).
- Many TCP conversations with 1-3 packets each = SYN scans or failed connections.
- Asymmetric bytes (A->B huge, B->A tiny) = upload/exfiltration or backup.

## Verify
- [ ] You can name the top 5 conversations by bytes and their applications.
- [ ] Protocol Hierarchy has no unexplained "Data" or legacy protocols left unexplained.
