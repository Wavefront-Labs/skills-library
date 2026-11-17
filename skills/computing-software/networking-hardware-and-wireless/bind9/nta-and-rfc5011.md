---
id: computing-software.networking-hardware-and-wireless.bind9.nta-and-rfc5011
name: nta-and-rfc5011
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, nta, rfc5011, managed-keys]
level: advanced
status: docs-checked
description: "BIND 9 negative trust anchors with rndc nta and nta-lifetime, and RFC 5011 managed trust anchors with standby KSKs."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter5.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nta and rfc5011
A negative trust anchor (NTA) makes named treat a zone as insecure instead of bogus when validation fails through misconfiguration rather than attack:

```
rndc nta example.com
```

`nta-lifetime` sets the default lifetime in seconds. `rndc nta` manages NTAs and `rndc secroots` lists trust anchors.

RFC 5011 lets a resolver track key changes without operator edits. Use `initial-key` in `trust-anchors`. The zone owner can add a stand-by key in advance; named stores it and moves to it when the original key is revoked. `dnssec-revoke` sets the REVOKED bit and writes a new key file pair.

## Checked

2026-11-04. Read the nta-lifetime entry, the Trust Anchors section and the dnssec-revoke man page: NTA purpose, lifetime in seconds, initial-key behaviour, stand-by key and the REVOKED bit confirmed. Removed an unconfirmed 30-day acceptance period, a key ID claim and an rndc managed-keys claim.

Method: documentation only; no commands were run.
