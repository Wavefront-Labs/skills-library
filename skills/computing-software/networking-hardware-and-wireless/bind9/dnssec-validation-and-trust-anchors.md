---
id: computing-software.networking-hardware-and-wireless.bind9.dnssec-validation-and-trust-anchors
name: dnssec-validation-and-trust-anchors
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, dnssec-validation, trust-anchors, root-key]
level: practitioner
status: docs-checked
description: "BIND 9 DNSSEC validation: dnssec-validation auto, trust-anchors block, static versus initial keys, SERVFAIL on failure."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter5.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnssec validation and trust anchors
Validation is on by default (`dnssec-validation auto`), with the root key built in and maintained through RFC 5011. A failed validation returns SERVFAIL.

A `trust-anchors` block supplies other keys. Types: `static-key`, `initial-key`, `static-ds`, `initial-ds`. Do not mix static and initial entries for the same name.

```
trust-anchors {
    example.net. initial-key 257 3 13 "base64-key";
};
```

`validate-except` lists names where validation is skipped permanently, for local-only top-level domains. An "insecurity proof failed" error means the parent is unsigned but the child claims DNSSEC.

## Checked

2026-11-04. Read the dnssec-validation, validate-except and trust-anchors entries in the Administrator Reference Manual and the DNSSEC chapter (Validation Failures). SERVFAIL, the insecurity-proof error text, auto/RFC 5011 behaviour and the no-mixing rule confirmed. Nothing was removed.

Method: documentation only; no commands were run.
