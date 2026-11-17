---
id: computing-software.networking-hardware-and-wireless.unbound.dnssec-validator-tuning
name: dnssec-validator-tuning
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, dnssec, val-sig-skew, val-bogus-ttl, nsec3-iterations, val-max-restart]
level: advanced
status: docs-checked
description: "Adjust Unbound DNSSEC validation behaviour: signature clock skew, bogus TTL, NSEC3 iteration limits, additional-section cleaning and validator restarts."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnssec validator tuning
- `val-sig-skew-min` (3600 s) and `val-sig-skew-max` (86400 s): clock-skew allowance for signatures, computed as 10% of signature lifetime and capped by these values.
- `val-bogus-ttl` (60 s): TTL for bogus data, replacing its untrusted TTL to prevent repeated revalidation.
- `val-clean-additional` (no): removes improperly signed data from the additional section of secure messages.
- `val-max-restart` (5): times the validator restarts with another authority after failure.
- `val-nsec3-keysize-iterations`: quoted keysize/iteration pairs in ascending order, default `"1024 150 2048 150 4096 150"`; higher iteration counts are marked insecure. `"1024 65535"` removes the restriction.
- `val-override-date` (0, disabled): debug only; -1 ignores dates.
- `harden-dnssec-stripped` (yes) makes a zone bogus when DNSSEC data is missing; disabling it may allow downgrade.
- `harden-algo-downgrade` (no) requires signatures from all DS algorithms; violates RFC 6840 and is for troubleshooting.

## Checked
2026-11-04. Confirmed against the unbound.conf manual: val-sig-skew-min/max, val-bogus-ttl, val-clean-additional, val-max-restart, val-nsec3-keysize-iterations, val-override-date, harden-dnssec-stripped and harden-algo-downgrade. Removed the fast_reload +p statement, which the unbound-control page does not support.
Method: documentation only; no commands were run.
