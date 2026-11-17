---
id: computing-software.networking-hardware-and-wireless.bind9.dnssec-policy-basics
name: dnssec-policy-basics
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, dnssec-policy, kasp, inline-signing]
level: practitioner
status: docs-checked
description: "Turn on automatic DNSSEC signing in BIND 9 with dnssec-policy default, key files, inline-signing and the insecure policy for unsigning."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter5.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dnssec policy basics
`dnssec-policy default;` in a zone enables automatic signing and key management (KASP). The built-in policies are `default` (a single CSK using ECDSAP256SHA256, no lifetime limit), `insecure` (used to unsign) and `none`.

```
zone "example.com" {
    type primary;
    file "example.com.db";
    dnssec-policy default;
};
```

This needs `inline-signing` (the default) or a dynamic zone. Keys are written as `K<name>+<alg>+<tag>.key` and `.private`. Revert to unsigned by switching the zone to the `insecure` policy before removing the policy. ZSK rollovers are automatic; KSK and CSK rollovers need a DS update at the parent.

## Checked

2026-11-04. Read the DNSSEC chapter (Easy-start Guide, key rollovers, Reverting to Unsigned) and the dnssec-policy block definition: built-in policies, inline-signing requirement, key file names, insecure policy and DS update requirement confirmed. Removed an unconfirmed .state file claim.

Method: documentation only; no commands were run.
