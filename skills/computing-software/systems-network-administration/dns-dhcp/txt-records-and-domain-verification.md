---
id: computing-software.systems-network-administration.dns-dhcp.txt-records-and-domain-verification
name: txt-records-and-domain-verification
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns-records, txt-record, domain-verification, character-strings, apex-txt-sprawl]
level: practitioner
status: verified
description: "Manage TXT records: 255-byte string splitting, quoting per provider, SaaS domain-verification tokens, keeping the apex TXT set small, and cleaning stale entries safely."
sources:
  - https://www.rfc-editor.org/rfc/rfc1035#section-3.3.14
  - https://www.rfc-editor.org/rfc/rfc7208#section-3.3
  - https://www.rfc-editor.org/rfc/rfc6376
  - https://www.rfc-editor.org/rfc/rfc8555
  - https://www.dnsflagday.net/2020/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TXT records and domain verification

## Format
A TXT record holds one or more character-strings, each max 255 bytes. Long values (DKIM keys,
long SPF) must be split; resolvers concatenate the strings for SPF/DKIM:
```
selector1._domainkey  IN TXT ( "v=DKIM1; k=rsa; p=MIIBIjANBgkqh...first255..."
                               "...remaining-part" )
```
Strings are joined with no whitespace added (RFC 6376 section 3.6.2.2 for DKIM, RFC 7208 section 3.3
for SPF), so split inside a value, not at a space you need. When a 300-character string was loaded
from a zone file, CoreDNS 1.15 stored it as a 255-byte and a 45-byte string. Always check what was
actually published with dig (or dnspython `rdata.strings`).
```
dig TXT selector1._domainkey.example.net +short
```

## Domain verification tokens
Many SaaS vendors (mail, identity, collaboration, signing) ask for a TXT record at the apex to prove
you control the domain; follow each vendor's current instructions. Prefer a dedicated label when the
vendor supports one (ACME uses `_acme-challenge.<name>`, RFC 8555 section 8.4): it keeps the apex
small.

## Apex TXT sprawl
Every lookup of TXT at the apex (SPF checks do this for every inbound email) returns all apex TXT
records. Dozens of stale verification strings push the response past the 1232-byte EDNS size that
DNS Flag Day 2020 recommends, which means truncation and TCP fallback, and RFC 7208 section 3.4 says
the SPF record should stay small enough that the answer fits in 512 octets. Keep it lean:
- Inventory: `dig TXT example.net +short`.
- Remove tokens for services no longer used, and tokens the vendor no longer needs after
  verification (check the vendor's docs first).
- Only one SPF record (`v=spf1`) may exist; two is a permerror.

## Change safely
- Lower the TTL before edits if you might need to revert quickly.
- Record ownership and purpose of each TXT in your DNS-as-code repo comments.

## Verify
- [ ] `dig TXT example.net` response well under 1232 bytes, exactly one SPF record (two gave
  `permerror` in a pyspf test), and each remaining token has an owner.
