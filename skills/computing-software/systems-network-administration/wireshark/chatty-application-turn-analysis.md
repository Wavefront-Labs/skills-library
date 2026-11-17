---
id: computing-software.systems-network-administration.wireshark.chatty-application-turn-analysis
name: chatty-application-turn-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, chatty-application, application-turns, latency, performance-analysis]
level: practitioner
status: verified
description: "Quantify chatty applications in captures by counting request/response turns and multiplying by RTT to show why WAN latency makes them slow."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChStatConversations.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chatty applications and turn counts

An application that needs 2,000 sequential round trips takes 2,000 x RTT regardless of bandwidth.
At 1 ms LAN RTT that is 2 s; at 40 ms WAN it is 80 s.

## Count turns
A turn is one request followed by waiting for a response. For SMB, SQL (TDS), LDAP, HTTP/1.1:
```
tshark -r app.pcapng -Y "smb2.flags.response == 0" | wc -l
tshark -r app.pcapng -Y "tds.type == 1" | wc -l           # SQL batches
tshark -r app.pcapng -Y "http.request" | wc -l
```
Generic: count direction changes in a TCP stream with data:
```
tshark -r app.pcapng -Y "tcp.stream==3 && tcp.len>0" -T fields -e ip.src | uniq | wc -l
```

## Compute the latency cost
```
turns x RTT = minimum time
```
Compare with the total transaction time (first to last packet). If turns x RTT is most of it,
the application design is the bottleneck, not bandwidth.

## Visual check
I/O Graph or Flow Graph shows a "picket fence" of small exchanges with idle gaps of one RTT each.
Statistics > Conversations shows small byte counts with long durations.

## Remedies (for the report)
- Move client near the server (VDI/terminal services), or the server near the clients.
- Application changes: batching, stored procedures, larger reads, HTTP/2 multiplexing.

## Verify
- [ ] Test from a low-latency location: duration scales with RTT as predicted by the turn count.

## Checked
Run on Wireshark 4.4.1: the `http.request` count, the `tcp.stream==N && tcp.len>0` direction-change count (3 changes for
a request, response, request exchange) and the arithmetic (turns x RTT) were run on a synthetic capture; `smb2.flags.response`
and `tds.type` exist and value 1 is "SQL batch" in `tshark -G values`. The remedies list is design guidance (WAN-optimisation and SMB-dialect remedies were removed because they were not checked).
