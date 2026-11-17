---
id: computing-software.systems-network-administration.dns-dhcp.dns-over-quic
name: dns-over-quic
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [encrypted-dns, doq, dns-over-quic, rfc9250, adguard, kdig, udp-853]
level: practitioner
status: verified
description: "Understand and deploy DNS over QUIC (RFC 9250): UDP 853, ALPN doq, server and client support, testing with kdig and q, and firewall implications versus DoT and DoH."
sources:
  - https://www.rfc-editor.org/rfc/rfc9250
  - https://www.knot-dns.cz/docs/latest/html/man_kdig.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS over QUIC (DoQ)

DoQ (RFC 9250) carries DNS messages over QUIC streams on UDP port 853 with ALPN `doq`. It offers
DoT's privacy with lower connection setup latency (0-RTT resumption) and no head-of-line blocking
between queries.

## Where it is used
- RFC 9250 covers stub to recursive, recursive to authoritative and zone transfer (section 5.7). Check each
  client platform's own documentation before assuming OS-level DoQ support; the tools below are the ones confirmed.

## Server software
- Knot DNS 3.3+ (authoritative; full DoQ without XDP arrived in 3.3.0): `server: listen-quic: 0.0.0.0@853` (default
  port 853, restart needed to change).
- dnsdist 1.9+ `addDOQLocal(address, certFile, keyFile)`.
- Unbound 1.22+: `quic-port: 853` (and `quic-size`), only in a build with libngtcp2 (`--with-libngtcp2`,
  needs OpenSSL with QUIC support); `quic-port: 0` disables it.
- CoreDNS: a server block `quic://.:853 { tls cert.pem key.pem ... }`. Run with CoreDNS 1.15.0 on Windows using
  `quic://.:8853` and a self-signed key: a dnspython 2.9 `dns.query.quic(..., verify=False)` query (needs `aioquic`)
  returned the `hosts` answer with RCODE 0.
- BIND 9: no DoQ in the ARM of 9.20 or the main branch (it has DoT and DoH).

## Testing
```
kdig @dns.example.net +quic example.com                  # Knot kdig 3.2+ (+quic first appeared in 3.2.0)
q example.com @quic://dns.example.net                    # natesales/q lists DNS over QUIC (RFC 9250)
```
In dnspython use `dns.query.quic(message, where, port=853)` (dnspython 2.9, needs `aioquic`).

## Firewall and policy
- Requires UDP 853 outbound; many enterprises allow only TCP 853 (DoT) or nothing. Blocking UDP
  853 forces clients to fall back (or fail), similar to blocking UDP 443 to disable QUIC/HTTP3.
- Like DoH, it bypasses enterprise resolvers and their filtering if allowed; include it in DNS
  egress policy (block UDP/TCP 853 except from your resolvers).
- Traffic is indistinguishable from other QUIC except by port; on 853 it is easy to identify.

## Gotchas
- Path MTU: RFC 9000 requires client UDP datagrams carrying Initial packets to have payloads of at least 1200
  bytes, so paths that drop that size or filter fragments cause failures.
- Certificates: same requirements as DoT (name must match what clients configure).

## Verify
- [ ] `kdig +quic` to your DoQ endpoint returns answers, and egress policy blocks DoQ to external
  resolvers from client networks.
