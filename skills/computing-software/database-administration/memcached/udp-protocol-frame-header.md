---
id: computing-software.database-administration.memcached.udp-protocol-frame-header
name: udp-protocol-frame-header
category: computing-software
field: database-administration
product: memcached
tags: [udp, udp-protocol, frame-header, datagram, u]
level: advanced
status: docs-checked
description: "The memcached UDP interface: 8-byte frame header, request IDs, multi-datagram responses, and when UDP is appropriate."
sources:
  - https://github.com/memcached/memcached/blob/master/doc/protocol.txt
  - https://docs.memcached.org/features/flashstorage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

UDP exists for very large installs where TCP connection counts hurt. Delivery is not guaranteed, so use it for operations that may fail, typically small `get`s where a missing response counts as a miss. It is off by default since 1.5.6; `-U` sets the UDP port and `-U 0` disables it.

Each datagram starts with an 8-byte header (16-bit values, network byte order):
```
0-1 request ID
2-3 sequence number (0..n-1)
4-5 total datagrams in this message
6-7 reserved, must be 0
```
The request ID is chosen by the client and echoed by the server; discard datagrams with unknown IDs (late replies). Concatenate payloads by sequence number to get the TCP-format response.

Requests must fit in one datagram; responses may span several. Huge multigets and sets belong on TCP.

Flash storage: UDP is not supported for objects flushed to disk.

Security: see disable-udp-ddos-hardening.

## Checked

Confirmed 2026-11-09: purpose and non-guaranteed delivery, the 8-byte header layout in network byte order, client-chosen request ID echoed by the server and discarding unknown IDs, sequence numbering and concatenation, single-datagram requests with multi-datagram responses (protocol.txt UDP protocol); UDP off by default since 1.5.6 and `-U 0` (Configuring page); no UDP for objects flushed to disk (Flash Storage page). Replaced the unsupported "enable with -U port" wording.

Method: docs-checked 2026-11-09 against memcached doc/protocol.txt and docs.memcached.org Configuring and Flash Storage pages
