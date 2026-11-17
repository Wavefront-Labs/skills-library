---
id: computing-software.systems-network-administration.dns-dhcp.naptr-records-for-sip-and-enum
name: naptr-records-for-sip-and-enum
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, naptr, enum, sip, srv-record, rfc3403]
level: practitioner
status: verified
description: "Write and debug NAPTR records for SIP service discovery and ENUM: order/preference, flags, services, regexp/replacement and the NAPTR-SRV-A chain."
sources:
  - https://www.rfc-editor.org/rfc/rfc3403
  - https://www.rfc-editor.org/rfc/rfc3263
  - https://www.rfc-editor.org/rfc/rfc6116
  - https://www.rfc-editor.org/rfc/rfc3404
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAPTR

NAPTR (type 35) maps a name to a URI or to another lookup, chained with SRV in SIP and ENUM.

## Format
```
example.com. IN NAPTR order pref "flags" "service" "regexp" replacement
example.com. IN NAPTR 10 10 "S" "SIPS+D2T" "" _sips._tcp.example.com.
example.com. IN NAPTR 20 10 "S" "SIP+D2T"  "" _sip._tcp.example.com.
example.com. IN NAPTR 30 10 "S" "SIP+D2U"  "" _sip._udp.example.com.
_sips._tcp.example.com. IN SRV 10 50 5061 sbc1.example.com.
```
- order: lower first, mandatory; pref: tie-break within an order.
- flags: defined by the application (RFC 3403 says the case of letters is not significant); RFC 3404
  defines `S` (next lookup is SRV), `A` (address), `U` (regexp yields a URI) and `P`; `""` means the
  next step is another NAPTR lookup.
- service: `SIP+D2U` (UDP), `SIP+D2T` (TCP), `SIPS+D2T` (TLS), `E2U+sip` (ENUM).
- regexp and replacement are mutually exclusive: one is empty (`""` / `.`).

## SIP resolution (RFC 3263)
Client looks up NAPTR for the domain, picks the transport it supports, follows to SRV, then A/AAAA.
Missing NAPTR: the client builds SRV queries (`_sip._udp`, `_sip._tcp`, `_sips._tcp`) for the transports
it supports; with no SRV it uses UDP for SIP and TCP for SIPS URIs, and with a numeric or non-SRV target
it looks up A/AAAA and uses the transport's default port (RFC 3263 sections 4.1 and 4.2).

## ENUM (RFC 6116)
+44 20 7946 0123 -> `3.2.1.0.6.4.9.7.0.2.4.4.e164.arpa.` (computed with `dns.e164.from_e164("+442079460123")`)
```
3.2.1.0.6.4.9.7.0.2.4.4.e164.arpa. IN NAPTR 100 10 "u" "E2U+sip" "!^.*$!sip:+442079460123@example.com!" .
```
Regexp delimiter `!` is conventional; `\\1` back-references groups.

## Debug
```
dig example.com NAPTR +short
dig _sips._tcp.example.com SRV +short
```
Common errors: unescaped backslashes in zone files (a single backslash before a digit is a syntax
error in dnspython; write two) and a missing trailing dot on the replacement. Flags are case
insensitive (RFC 3403).

## Verify
- [ ] A SIP client, or a manual chain of `dig` queries (NAPTR, then SRV, then A/AAAA), reaches the
  expected transport and target host.
