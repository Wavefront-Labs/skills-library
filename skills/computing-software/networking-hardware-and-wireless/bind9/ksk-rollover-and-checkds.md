---
id: computing-software.networking-hardware-and-wireless.bind9.ksk-rollover-and-checkds
name: ksk-rollover-and-checkds
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, ksk-rollover, checkds, parental-agents]
level: advanced
status: docs-checked
description: "Handle KSK and CSK rollover in BIND 9 with parental-agents, checkds, and rndc dnssec -checkds and -rollover."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter5.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ksk rollover and checkds
ZSK rollovers are automatic. KSK and CSK rollovers need the DS record at the parent to be updated, which named can check by querying the parent's servers.

```
parental-agents "parent" { /* parent server addresses */ };
zone "example.com" {
    dnssec-policy "custom";
    parental-agents { "parent"; };
    checkds explicit;
};
```

Commands:

- `rndc dnssec -checkds [-key id] published zone` or `withdrawn zone` tells named the DS has been confirmed published in, or withdrawn from, the parent zone. It is required to complete a KSK rollover; `checkds no` means you run it manually.
- `rndc dnssec -rollover -key id zone` schedules a rollover for a key, overriding its lifetime; it starts immediately unless `-when time` is given.
- `rndc dnssec -status zone` shows the DNSSEC signing state; `-v` adds key states.
- `dnssec-keygen -G` generates a key without publishing it or signing with it.

With `manual-mode yes` in the policy, rollovers are logged and proceed only after `rndc dnssec -step`.

## Checked

2026-11-04. Confirmed against the ARM `dnssec-policy`, `parental-agents`, `checkds` and `manual-mode` entries, the DNSSEC chapter on rollovers, and the rndc and dnssec-keygen man pages. Corrected the `-checkds`, `-rollover` and `-G` descriptions and removed the "pregenerates" wording.

Method: documentation only; no commands were run.
