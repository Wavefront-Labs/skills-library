---
id: computing-software.systems-network-administration.wireshark.follow-udp-quic-and-http2-streams
name: follow-udp-quic-and-http2-streams
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, follow-stream, follow-udp-stream, follow-http2-stream, quic, http2]
level: practitioner
status: verified
description: "Use Follow UDP, QUIC and HTTP/2 Stream in Wireshark and tshark -z follow to read one stream's payload, with stream index filters and decryption prerequisites."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Follow UDP/QUIC/HTTP2 streams

Follow Stream shows application payload of one conversation as the client and server saw it.

## UDP
Analyze > Follow > UDP Stream. Wireshark applies `udp.stream eq N`. A UDP
"stream" is just the 5-tuple; useful for syslog, SIP over UDP, TFTP, custom protocols.

## HTTP/2
Analyze > Follow > HTTP/2 Stream applies `tcp.stream eq N and http2.streamid eq M`. One TCP
connection carries many HTTP/2 streams; the dialog has a substream selector. Over TLS (the normal case for browsers) it needs
decrypted TLS (key log file); cleartext HTTP/2 (`h2c`, e.g. curl `--http2-prior-knowledge`) follows without keys.

## QUIC
Analyze > Follow > QUIC Stream filters `quic.connection.number eq N` and lets you choose the QUIC
stream ID (0, 4, 8 are client bidirectional streams). Requires `SSLKEYLOGFILE` keys; without them
there is no stream data to follow (tshark prints an empty result).

## tshark
```
tshark -r in.pcapng -q -z follow,udp,ascii,3
tshark -r in.pcapng -q -z follow,http2,ascii,0,1          # tcp stream 0, h2 stream 1
tshark -r in.pcapng -q -z follow,quic,raw,2,0
tshark -r in.pcapng -q -z follow,tcp,hex,10.1.1.5:51234,10.2.2.2:443
```
Modes: ascii, hex, raw, yaml, ebcdic (all ran in 4.4.1).

## Reading the dialog
- Client data is red and server data blue by default (set by the theme); "Entire conversation" or one direction.
- Following applies a display filter selecting the stream; closing the dialog with Back resets it (User's Guide).

## Gotchas
- HPACK header compression (RFC 7541) keeps a dynamic table per connection, so headers in a capture that starts mid-connection may not decode; capture from the connection start.
- Follow replaces your display filter with the stream filter; save the original as a filter button first.

## Verify
- [ ] The followed content matches the object exported via File > Export Objects for the same stream.

## Checked
Run on Wireshark 4.4.1: `follow,udp,ascii,N` and `follow,udp,raw,N` printed the stream with the `udp.stream eq N` filter; a cleartext
HTTP/2 capture (prior-knowledge preface, two request streams) was decoded and `follow,http2,ascii,0,1` printed the
stream with the filter `tcp.stream eq 0 and http2.streamid eq 1` (tcp stream 0, h2 stream 1); `follow,tcp,hex,<ip:port>,<ip:port>`,
`yaml` and `ebcdic` ran; `follow,quic,raw,0,0` produced the filter `quic.connection.number eq 0 and quic.stream.stream_id eq 0`
(no data without keys). Client-initiated bidirectional QUIC streams are IDs 0, 4, 8 per RFC 9000. Colours, the Back button and the
HTTP/2 substream field are in the User's Guide Follow chapter.
