---
id: computing-software.networking-hardware-and-wireless.bind9.nsec3-config
name: nsec3-config
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, nsec3, nsec3param, opt-out]
level: advanced
status: docs-checked
description: "Switch a BIND 9 dnssec-policy from NSEC to NSEC3 with nsec3param and why to keep iterations and salt at zero."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nsec3 config
NSEC is the default. Add `nsec3param` to the `dnssec-policy` to use NSEC3:

```
nsec3param iterations 0 optout no salt-length 0;
```

All three parts are optional; unset values take those defaults. named generates the salt itself at the length you set.

The reference warns not to use extra iterations, salt or opt-out unless their implications are understood: more iterations cause interoperability problems and opens servers to CPU-exhausting DoS attacks (RFC 9276).

## Checked

2026-11-04. Read the nsec3param entry in the Administrator Reference Manual: grammar, default NSEC, optional parts and the named-generated salt confirmed. Reworded the iterations warning to match the page.

Method: documentation only; no commands were run.
