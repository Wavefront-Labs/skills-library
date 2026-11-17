---
id: computing-software.networking-hardware-and-wireless.bind9.closed-recursive-resolver
name: closed-recursive-resolver
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, resolver, recursion, allow-query]
level: practitioner
status: docs-checked
description: "Configure a BIND 9 caching resolver restricted to internal clients using an acl, recursion yes and allow-query."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter3.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# closed recursive resolver
A closed resolver answers recursive queries only for trusted networks:

```
acl corpnets { /* internal networks */ };
options {
    recursion yes;
    allow-query { corpnets; };
};
```

Reference the `acl` by name in `allow-query`. Only clients in the listed networks are allowed.

## Checked

2026-11-04. Confirmed against the ARM Configuration chapter caching-resolver example: `acl`, `recursion yes`, `allow-query` referencing the acl by name. Removed the unconfirmed claim about outside clients being refused.

Method: documentation only; no commands were run.
