---
id: computing-software.networking-hardware-and-wireless.unbound.domain-insecure-exceptions
name: domain-insecure-exceptions
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, domain-insecure, dnssec, insecure-add, negative-trust-anchor, internal-zones]
level: practitioner
status: docs-checked
description: "Exempt a domain from DNSSEC validation in Unbound with domain-insecure, at config time or at runtime with unbound-control."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# domain insecure exceptions
`domain-insecure: <domain>` treats the domain as unsigned, ignoring the DNSSEC chain of trust for it even if a trust anchor exists above. It can be repeated. An explicit trust anchor for that domain overrides it.

Runtime:
- `unbound-control insecure_add zone` adds an entry; it does not clear cached data or change the config file.
- `insecure_remove zone` removes it.
- `list_insecure` lists the entries.
- `forward_add +i` and `stub_add +i` add a domain-insecure entry with the zone; `forward_remove +i` and `stub_remove +i` remove it.

Related reverse-zone behaviour: `insecure-lan-zones` skips validation for private-address reverse zones.

If a zone's failure is a validation problem rather than an unsigned zone, find the cause with `val-log-level` first; see dnssec-failure-diagnosis-and-permissive-mode.

## Checked

2026-11-08. Read domain-insecure in the unbound.conf manual and insecure_add, insecure_remove, list_insecure, forward_add, forward_remove, stub_add and stub_remove in the unbound-control manual. Claims confirmed.

Method: documentation only; no commands were run.
