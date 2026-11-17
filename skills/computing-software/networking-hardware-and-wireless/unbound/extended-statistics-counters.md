---
id: computing-software.networking-hardware-and-wireless.unbound.extended-statistics-counters
name: extended-statistics-counters
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, extended-statistics, histogram, rcode, memory-counters, bogus]
level: advanced
status: docs-checked
description: "Read Unbound extended statistics: memory, latency histogram, query type and transport, rcodes, validation, unwanted traffic and per-feature counters."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# extended statistics counters
Enabled by `extended-statistics: yes`; zero-valued ones may be hidden by `statistics-inhibit-zero` (default yes).

- Memory: `mem.cache.rrset`, `mem.cache.message`, `mem.mod.iterator`, `mem.mod.validator`, `mem.streamwait`, `mem.http.query_buffer`, `mem.http.response_buffer`, `mem.quic`.
- Latency: `histogram.<sec>.<usec>.to.<sec>.<usec>`, 40 buckets with doubling widths, counting recursive replies.
- Queries: `num.query.type.A` etc., `num.query.class.*`, `num.query.opcode.*`, `num.query.flags.RD` etc., `num.query.edns.present` and `.DO`, `num.query.ipv6`.
- Transport: `num.query.tcp`, `.tls`, `.tls.resume`, `.https`, `.quic`, and outgoing `num.query.tcpout`, `.udpout`. Counts nest: TLS queries are also in `tcp`, HTTPS also in `tcp` and `tls`, QUIC also in `tls`.
- Answers: `num.answer.rcode.NXDOMAIN` etc., `num.answer.rcode.nodata`, `num.answer.secure`, `num.answer.bogus`, `num.rrset.bogus`, `num.valops`.
- Unwanted: `unwanted.queries` (access control), `unwanted.replies` (possible spoofing if high).
- Sizes: `msg.cache.count`, `rrset.cache.count`, `infra.cache.count`, `key.cache.count`, `*.max_collisions` (hundreds suggest a problem).
- Features: `num.query.authzone.up`/`.down`, `num.query.aggressive.*`, `num.query.subnet`, `num.query.cachedb`, `num.rpz.action.<action>`.

## Checked

2026-11-08. Read the whole Extended Statistics section of the unbound-control manual and statistics-inhibit-zero in unbound.conf. Counter names confirmed; added the nesting of TLS, HTTPS and QUIC counts.

Method: documentation only; no commands were run.
