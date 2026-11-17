---
id: computing-software.networking-hardware-and-wireless.bind9.update-policy-rules
name: update-policy-rules
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, update-policy, grant, self]
level: advanced
status: docs-checked
description: "Write BIND 9 update-policy rules: grant or deny identity, rule types such as name, subdomain, zonesub, self and selfsub, and type lists."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# update policy rules
`update-policy` replaces `allow-update` with fine-grained rules. Each rule is `(grant | deny) identity ruletype name types`.

Rule types include `name`, `subdomain`, `zonesub`, `wildcard`, `self`, `selfsub`, `selfwild`, `tcp-self`, `6to4-self`, `external`, and the `ms-*` and `krb5-*` families. Types can carry limits such as `PTR(1)`.

```
update-policy {
    grant host1-host2. name host.example.com. A AAAA;
};
```

`update-policy local;` enables local updates with `session-keyfile`, `session-keyname` and `session-keyalg` controlling the generated key. Rules are checked in order and the first match decides.

## Checked

2026-11-04. Read the update-policy section of the Administrator Reference Manual: rule form, rule type list, type limits such as PTR(1), update-policy local with session-key options, and first-match ordering. Nothing was removed.

Method: documentation only; no commands were run.
