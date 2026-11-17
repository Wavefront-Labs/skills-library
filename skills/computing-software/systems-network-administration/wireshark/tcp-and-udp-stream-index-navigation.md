---
id: computing-software.systems-network-administration.wireshark.tcp-and-udp-stream-index-navigation
name: tcp-and-udp-stream-index-navigation
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcp-stream-index, udp-stream, conversation-filter, tshark-fields, stream-analysis]
level: practitioner
status: verified
description: "Use tcp.stream and udp.stream indexes to isolate and iterate conversations: filters, tshark loops per stream, stream-aware columns, and pitfalls with port reuse."
sources:
  - https://www.wireshark.org/docs/dfref/t/tcp.html
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Navigating by stream index

Wireshark numbers every TCP connection (`tcp.stream`) and UDP 5-tuple flow (`udp.stream`) from 0 in
order of first appearance. It is the fastest way to isolate a conversation.

## In the GUI
```
tcp.stream eq 42
tcp.stream in {42, 57, 101}      # commas required: the space-separated form is a syntax error in 4.4.1
udp.stream eq 7
quic.connection.number eq 3
```
Right-click > Conversation Filter > TCP generates the same. Follow Stream has a spin box to step to
the next/previous stream. Add a `tcp.stream` column to see boundaries while scrolling.

## Per-stream processing with tshark
```
# list streams with first packet time and endpoints
tshark -r cap.pcapng -Y "tcp.flags.syn==1 && tcp.flags.ack==0" -T fields \
  -e tcp.stream -e frame.time -e ip.src -e ip.dst -e tcp.dstport

# extract each HTTP stream to its own file
for s in $(tshark -r cap.pcapng -Y http.request -T fields -e tcp.stream | tr -d '\r' | sort -un); do   # tr: tshark on Windows prints CRLF
  tshark -r cap.pcapng -Y "tcp.stream eq $s" -w stream_$s.pcapng
done

# follow one stream as ASCII
tshark -r cap.pcapng -q -z follow,tcp,ascii,42
```
(Run: `tcp.stream eq`, the comma set form, the SYN listing and `follow,tcp,ascii,0` all worked; `udp.stream` numbered
each UDP 5-tuple.)
For many streams, one pass that writes per-stream files is faster than re-reading the capture each
time; use `editcap` on frame ranges or a small script with pyshark/scapy.

## Pitfalls
- Index values depend on the file: splitting or filtering a capture renumbers streams. Do not quote
  stream numbers across different files; quote 5-tuple and time.
- Port reuse: a new SYN on the same 4-tuple after the old connection closed gets a new index, marked
  `[TCP Port numbers reused]` (seen in a run), but captures that start mid-connection may merge oddly.
- `udp.stream` is just a 5-tuple; DNS clients reusing a source port make many queries one "stream".

## Verify
- [ ] Filtering on the index returns exactly one SYN (for complete TCP streams) and both directions
  of traffic.
