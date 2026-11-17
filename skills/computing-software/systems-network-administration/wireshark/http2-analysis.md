---
id: computing-software.systems-network-administration.wireshark.http2-analysis
name: http2-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, http2, alpn, hpack, grpc, rst-stream, goaway, tls-decryption]
level: practitioner
status: verified
description: "Analyse HTTP/2 in Wireshark: decrypt and confirm h2 via ALPN, read streams/HEADERS/DATA frames, decode gRPC, and diagnose RST_STREAM, GOAWAY and flow-control stalls."
sources:
  - https://www.rfc-editor.org/rfc/rfc9113
  - https://www.wireshark.org/docs/dfref/h/http2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP/2 analysis

## Get it decoded
HTTP/2 almost always runs over TLS. Load keys (SSLKEYLOGFILE) first. Confirm negotiation:
```
tls.handshake.extensions_alpn_str == "h2"
```
Cleartext h2c (gRPC inside clusters, port 50051/8080): if the connection preface (`PRI * HTTP/2.0`) is in the capture,
TShark 4.4.1 recognised h2c and gRPC with no setup; for a capture that starts mid-connection use Decode As TCP port
-> HTTP2 (`-d tcp.port==8080,http2`).

## Structure
One TCP connection, many streams (client-initiated streams use odd IDs, RFC 9113 section 5.1.1). Frames: HEADERS, DATA, SETTINGS,
WINDOW_UPDATE, PING, RST_STREAM, GOAWAY, PRIORITY.
```
http2.streamid == 5
http2.type == 1                          # HEADERS
http2.headers.path contains "/api/"
http2.headers.status == "503"
http2.type == 3                          # RST_STREAM
http2.type == 7                          # GOAWAY
```
Follow > HTTP/2 Stream shows one request/response; Statistics > HTTP2 gives frame counts (`tshark -q -z http2,tree`).

## gRPC
Wireshark decodes gRPC on top of HTTP/2 (`grpc`, `grpc.message_length`); add .proto files in
Preferences > Protocols > Protobuf > Protobuf search paths (a table in the User's Guide) to decode message fields. `grpc-status` trailer
(in a final HEADERS frame) carries the gRPC error code; HTTP status stays 200. There is no dedicated field in
4.4.1: use `http2.header.name == "grpc-status"` and read `http2.header.value` (14 = UNAVAILABLE in the gRPC status
codes).

## Diagnosing problems
Names and numbers come from `tshark -G values`; meanings follow RFC 9113.
| Seen | Meaning |
|---|---|
| RST_STREAM error CANCEL (8) | the stream is no longer needed; usually the client gave up (timeout, navigation) |
| RST_STREAM REFUSED_STREAM (7) | the endpoint refused the stream before any application processing, e.g. when the concurrent-stream limit was exceeded (RFC 9113 sections 5.1.2 and 7); the request is safe to retry |
| GOAWAY (`http2.goaway.last_stream_id`, `http2.goaway.error`) | server closing connection gracefully (deploy, idle); requests with higher IDs must retry |
| GOAWAY ENHANCE_YOUR_CALM (11) / PROTOCOL_ERROR (1) | the sender says its peer shows behaviour that may generate excessive load (ENHANCE_YOUR_CALM, RFC 9113) or violated the protocol |
| DATA stops, no WINDOW_UPDATE from receiver | flow-control window exhausted: slow consumer |
| Long gap between HEADERS and DATA on server side | delay before the server produced data (often the backend) |

Check SETTINGS frames for `SETTINGS_MAX_CONCURRENT_STREAMS` and `INITIAL_WINDOW_SIZE`; small windows
throttle high-latency transfers.

## Gotchas
- HPACK is stateful: if the capture starts mid-connection, indexed headers cannot be resolved and show as
  `Header: <unknown>:` in 4.4.1 (checked with a request that referenced a dynamic-table entry whose definition was
  missing). Capture from connection start.
- One lost TCP segment blocks all streams (head-of-line); compare with HTTP/3 over QUIC.

## Verify
- [ ] Each failing request maps to a stream ID with its :path, :status (or grpc-status) and timing.

## Checked
Run with TShark 4.4.1 on a hand-built h2c/gRPC capture (preface, SETTINGS, HEADERS with `:path /pkg.Svc/Call`, a gRPC
DATA message, a second request followed by RST_STREAM CANCEL, a 200 response with a trailing `grpc-status: 14` HEADERS
frame, GOAWAY ENHANCE_YOUR_CALM): every filter in the Structure list matched the expected frames (`http2.streamid == 3`
1, `http2.type == 1` 2, `http2.type == 3` 1, `http2.type == 7` 1, `contains "/api/"` 1), `grpc.message_length`
present, `-z http2,tree` counts (4 HEADERS, 3 SETTINGS, 1 each RST_STREAM, GOAWAY, DATA). Error names and numbers
(CANCEL 8, REFUSED_STREAM 7, ENHANCE_YOUR_CALM 11, PROTOCOL_ERROR 1; frame types 0-9) read from `tshark -G values`; odd
stream ids from RFC 9113 5.1.1. Stateful-HPACK test described in the Gotchas. Backend-latency, flow-control and
meanings in the diagnosis table are paraphrased from RFC 9113 section 7 (CANCEL, REFUSED_STREAM, ENHANCE_YOUR_CALM).
