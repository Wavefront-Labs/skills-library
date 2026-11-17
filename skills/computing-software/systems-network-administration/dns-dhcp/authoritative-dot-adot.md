---
id: computing-software.systems-network-administration.dns-dhcp.authoritative-dot-adot
name: authoritative-dot-adot
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, adot, dns-over-tls, authoritative-dns, encrypted-dns, certificates]
level: practitioner
status: docs-checked
description: "Offer DNS over TLS on authoritative servers (ADoT) per RFC 9539: how resolvers probe port 853, accept any certificate, fall back, and what servers should do under load."
sources:
  - https://www.rfc-editor.org/rfc/rfc9539
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authoritative DoT (opportunistic, RFC 9539)

Most DoT/DoH protects stub-to-resolver traffic. RFC 9539 (Experimental) describes opportunistic encryption of recursive-resolver-to-authoritative queries on port 853 without coordination between the two sides. It defends only against passive observers.

## How resolvers behave
- DoT uses TCP 853 with ALPN `dot`; resolvers MUST implement DoT or DoQ as clients and SHOULD implement both.
- They send Do53 and encrypted queries concurrently (Happy-Eyeballs style) and track success per authoritative IP address.
- After encrypted transport recently succeeded (suggested persistence 3 days) they stop using Do53 for that server.
- On handshake failure or timeout (suggested timeout 4 s) they fall back to Do53 and wait out a damping period (suggested 1 day). An active attacker can force this fallback.

## What it means for the server operator
- Listen for DoT on 853 in addition to Do53; keep port 53 working.
- No particular authentication is needed: a self-issued, regularly updated X.509 certificate is acceptable. Resolvers MUST accept any certificate (they may log failures but must not reject), so certificate validity does not gate adoption.
- Resolvers SHOULD NOT send SNI, and servers MUST NOT return different records based on SNI.
- RFC 9539 does not define SVCB signalling; it only notes a future protocol would need a signalling mechanism.
- Manage connections per RFC 9250 and RFC 7858. Under pressure close idle connections first (longest idle first), then those with outstanding queries (oldest query first).
- Pooled servers behind a load balancer or anycast should enable the same transports within about 30 seconds, or route by client IP, to avoid timeouts.
- Padding (RFC 7830, RFC 9250, RFC 8467), out-of-order responses and session resumption are recommended.

## Checked
Method: 2026-11-08 read RFC 9539 and kept only its claims. Removed as unverified against the pages read: BIND, Knot and NSD configuration snippets, named large-resolver adoption, ACME advice and the kdig/openssl test commands. BIND and Knot reference pages were dropped from sources unread.

## Verify
- [ ] A TLS handshake to the server on port 853 succeeds and answers an authoritative query, while port 53 still answers.
