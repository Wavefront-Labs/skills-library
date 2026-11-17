---
id: computing-software.networking-hardware-and-wireless.bind9.manual-dnssec-tools
name: manual-dnssec-tools
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, dnssec-keygen, dnssec-signzone, dnssec-settime]
level: practitioner
status: docs-checked
description: "Sign BIND 9 zones by hand with dnssec-keygen, dnssec-signzone, dnssec-settime and dnssec-verify instead of dnssec-policy."
sources:
  - https://bind9.readthedocs.io/en/latest/manpages.html
  - https://bind9.readthedocs.io/en/latest/chapter5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# manual dnssec tools
Manual tooling:

- `dnssec-keygen` creates keys; algorithms include RSASHA256, RSASHA512, ECDSAP256SHA256, ECDSAP384SHA384, ED25519 and ED448.
- `dnssec-signzone` signs a zone; `-S` is smart signing, which reads timing metadata from the key files.
- `dnssec-settime` edits key timing.
- `dnssec-verify` checks a signed zone.
- `dnssec-dsfromkey` makes DS records.

```
dnssec-keygen -K keys -f KSK -P now -A now+2y example.net
dnssec-signzone -S -K keys example.net
```

## Checked

2026-11-04. Read the dnssec-keygen, dnssec-signzone, dnssec-settime, dnssec-verify and dnssec-dsfromkey man pages: algorithm names, -f KSK, -P and -A date offsets, and smart signing (-S) confirmed. Removed two unconfirmed closing tips.

Method: documentation only; no commands were run.
