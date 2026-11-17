---
id: computing-software.networking-hardware-and-wireless.bind9.views-and-split-dns
name: views-and-split-dns
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, views, split-dns, match-clients]
level: advanced
status: docs-checked
description: "BIND 9 views for split DNS: match-clients, match-destinations, match-recursive-only, first-match order, and the all-zones-in-views rule."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/chapter6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# views and split dns
A `view` gives different clients different answers. Match options: `match-clients`, `match-destinations`, `match-recursive-only`. Views are tested in order and the first view a request matches resolves it, so order matters. A client matches when its source address fits `match-clients` and its destination address fits `match-destinations`; both default to all addresses and can also name a TSIG key. `match-recursive-only` means only recursive requests match. Only class IN is usable for views, and it is the default.

If any explicit view exists, all zone statements must occur inside views.

```
view "internal" {
    match-clients { internals; };
    recursion yes;
    zone "example.com" { type primary; file "internal/example.com.db"; };
};
view "external" {
    match-clients { any; };
    recursion no;
    zone "example.com" { type primary; file "external/example.com.db"; };
};
```

The same zone name can appear in several views with different files. Define `internals` as an `acl`.

## Checked

2026-11-04. Confirmed against the ARM view block entry (8.2.27): match options, defaults, TSIG key matching, first-view-wins, class IN only, all zones inside views, same zone name in several views. Removed the unconfirmed advice to put the most specific view first.

Method: documentation only; no commands were run.
