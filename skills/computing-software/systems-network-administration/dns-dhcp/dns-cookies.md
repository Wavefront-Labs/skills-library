---
id: computing-software.systems-network-administration.dns-dhcp.dns-cookies
name: dns-cookies
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns-security, dns-cookies, rfc7873, rfc9018, anycast-dns, spoofing, edns]
level: practitioner
status: gated
description: "Use DNS Cookies (RFC 7873/9018) against spoofing: client and server cookies, BIND and Unbound settings, shared secrets for anycast, and BADCOOKIE troubleshooting."
sources:
  - https://www.rfc-editor.org/rfc/rfc7873
  - https://www.rfc-editor.org/rfc/rfc9018
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS cookies

A lightweight EDNS option: the client sends a client cookie; the server replies with a server
cookie derived from the client IP and a server secret. Subsequent queries carrying a valid server
cookie prove the client really owns its source address (it saw the earlier reply), so a server can apply its own policy (discard, answer BADCOOKIE, or rate limit) to queries
without one while genuine clients are unaffected.

## See it
```
dig example.net @ns1.example.net +cookie
; COOKIE: 2464f7e1c4d1ba91010000006712...  (good)
```
`(good)` means the server validated the cookie; `(bad)` or missing server part means it did not.
(gated: unconfirmed, source is paywalled or blocked) The `(good)`/`(bad)` annotation is dig's own
output and dig is not available on the Windows review host, so it was not run. What is confirmed:
the cookie is EDNS option code 10, a client cookie is 8 bytes and a server cookie is 8 to 32 bytes
(RFC 7873); RFC 9018 gives the server cookie a fixed layout of 1-byte version, 3 reserved bytes,
4-byte timestamp and 8-byte hash, which is the shape of the 16-byte server part in the example.

## BIND
`answer-cookie` (send COOKIE options in replies to clients) defaults to yes; `send-cookie` controls
whether BIND sends a cookie when it queries other servers. Options:
```
options {
    require-server-cookie yes;      // default no: BADCOOKIE instead of a full UDP answer without a valid server cookie
    cookie-algorithm siphash24;     // the only supported value; the old "aes" option was removed
};
```
`require-server-cookie yes` is for servers answering clients: a cookie-aware client without a valid
server cookie gets a small BADCOOKIE reply and must repeat the query with the new cookie. The BIND
reference recommends it for testing client BADCOOKIE handling or when you are receiving many
forged queries that carry cookies, because the BADCOOKIE reply is smaller than a full answer.

## Anycast and server pools
BIND and Unbound generate a random secret at startup unless you set one, so another anycast
instance cannot validate a server cookie issued by this one: the client is given a fresh cookie
but loses the benefit. Share a 128-bit hex secret across instances:
```
options { cookie-secret "00112233445566778899aabbccddeeff"; };   // same value on all members
```
In BIND `cookie-secret` may be repeated: the first one listed generates new server cookies and the
others are only used to verify returned cookies, which is how you rotate. RFC 9018 standardises the
server cookie format (SipHash-2-4) so an anycast set of different implementations can interoperate.

## Unbound
```
server:
    answer-cookie: yes
    cookie-secret: "000102030405060708090a0b0c0d0e0f"
```
Unbound's `answer-cookie` defaults to no, so it must be enabled. `cookie-secret` defaults to a random
secret generated at startup and is ignored when a `cookie-secret-file` exists (Unbound manual).

## Troubleshooting
- RCODE 23 BADCOOKIE: the server did not accept the cookie (bad or missing). The reply carries a new
  server cookie and the client should retry with it (RFC 7873). Persistent BADCOOKIE suggests
  mismatched secrets in a pool or something altering EDNS options on the path.
- A middlebox that strips unknown EDNS options removes cookies silently; the client then simply
  gets no cookie protection.

## Verify
- [ ] A second query to each anycast instance, carrying the server cookie from the first, is
  accepted without BADCOOKIE.
