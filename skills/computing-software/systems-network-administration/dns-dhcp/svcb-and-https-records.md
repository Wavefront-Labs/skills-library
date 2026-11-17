---
id: computing-software.systems-network-administration.dns-dhcp.svcb-and-https-records
name: svcb-and-https-records
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, svcb, https-record, rfc-9460, alpn, ech, alias-mode, dns-records]
level: practitioner
status: verified
description: "Publish SVCB and HTTPS DNS records (RFC 9460): alias vs service mode, alpn h3 hints, ipv4hint/ipv6hint, ECH config, apex aliasing, and checking client use."
sources:
  - https://www.rfc-editor.org/rfc/rfc9460
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Alt-Svc
  - https://www.rfc-editor.org/rfc/rfc3597
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SVCB and HTTPS records

RFC 9460 defines SVCB (type 64) and its HTTPS-specific form **HTTPS** (type 65). HTTPS-aware
clients look up HTTPS alongside A/AAAA (RFC 9460 section 3) and learn, before connecting: which
protocols the server speaks (section 9.2 compares this with Alt-Svc), alternate endpoints, address
hints and ECH keys.

## Syntax
```
; ServiceMode: priority >= 1, target ("." = the owner name itself)
example.com.      3600 IN HTTPS 1 . alpn="h3,h2" ipv4hint=192.0.2.10 ipv6hint=2001:db8::10
; Alternative endpoint with lower preference
example.com.      3600 IN HTTPS 2 cdn.example.net. alpn="h2"
; AliasMode: priority 0, works at the zone apex (where CNAME cannot)
example.com.      3600 IN HTTPS 0 lb.provider.example.
www.example.com.  3600 IN HTTPS 1 . alpn="h3,h2" port=8443
```
Key parameters: `alpn`, `no-default-alpn`, `port`, `ipv4hint`, `ipv6hint`, `ech`
(Encrypted Client Hello config, base64), `mandatory`.

## Rules
- Hints are hints: clients still resolve A/AAAA of the target; keep them consistent or
  connections go to stale addresses.
- Advertising `h3` means UDP 443 must work end to end, or clients waste time and fall back.
- `ech=` must match what the TLS server actually serves; rotate both together.
- Requires an authoritative server that supports the type: BIND 9.16.21 or later (parsing and
  printing only, no additional-section processing, per its CHANGES file), PowerDNS Authoritative
  4.4.0 or later (its 4.4 changelog), and CoreDNS 1.15 served the examples here; for other servers
  or a managed DNS provider check the vendor's documentation. Servers without the type need RFC 3597
  generic syntax `TYPE65 \# ...`.
- Unsigned HTTPS/SVCB data can be altered by an on-path attacker; sign the zone. RFC 9460 section 3.1
  tells clients that get protected DNS (DNSSEC, DoT or DoH) answers to abandon the connection when
  SVCB resolution then fails, rather than fall back.

## Verify
```bash
dig example.com HTTPS +short
```
A packet capture shows the QTYPE 65 (HTTPS) query. What a browser does with the answer depends on
the browser and version, so test the clients you care about.
All four sample records above (apex ServiceMode with hints, an alternative endpoint, AliasMode and
`port=8443`) loaded in CoreDNS 1.15 and read back with dnspython, which printed them in the same
form (hints and port in quotes); the RFC 3597 generic form round-tripped to the same record.
- [ ] Record resolves from public resolvers, parameters match server capabilities, clients use h3/ECH as intended.
