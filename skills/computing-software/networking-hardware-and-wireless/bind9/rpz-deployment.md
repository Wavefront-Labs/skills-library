---
id: computing-software.networking-hardware-and-wireless.bind9.rpz-deployment
name: rpz-deployment
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, rpz-deployment, distribution-primary, walled-garden]
level: advanced
status: docs-checked
description: "Deploy RPZ feeds with BIND 9: a distribution primary with explicit notify, internal policy zones first, PASSTHRU rules for partners."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rpz deployment
The policy zone is a normal DNS zone synchronised with the usual zone transfer tools. Its primary can be an internal server you maintain, or an external server such as a security vendor's. An internal layout might look like this:

On the distribution primary:

```
zone "rpz.example.com" {
    type primary;
    file "rpz.example.com.db";
    notify explicit;
    also-notify { /* resolver addresses */ };
    allow-query { localhost; };
};
```

On each resolver, add the policy zone as a normal secondary zone and list it in `response-policy`. named can subscribe to up to 64 response policy zones.

## Checked

2026-11-04. Confirmed against the ARM RPZ chapter: policy zone as a normal zone listed in `response-policy`, internal or external primary, the 64-zone limit. Removed the zone-ordering and PASSTHRU advice, which the cited pages do not state.

Method: documentation only; no commands were run.
