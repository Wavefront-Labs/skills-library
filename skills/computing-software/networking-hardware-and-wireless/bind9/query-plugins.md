---
id: computing-software.networking-hardware-and-wireless.bind9.query-plugins
name: query-plugins
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, plugin, filter-aaaa, synthrecord]
level: advanced
status: docs-checked
description: "Load BIND 9 query plugins: plugin query syntax, filter-aaaa.so, filter-a.so, synthrecord.so, and where plugins can be scoped."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter4.html
  - https://bind9.readthedocs.io/en/latest/manpages.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# query plugins
Only query plugins exist. Syntax: `plugin query "library.so" { parameters };`. They can be set globally, in a view, or in a zone, and templates support them. Shipped with BIND: `filter-aaaa.so`, `filter-a.so`, `synthrecord.so`.

```
plugin query "filter-aaaa.so" {
    filter-aaaa-on-v4 yes;
    filter-aaaa { 192.0.2.1; 2001:db8:2::1; };
};
```

`filter-aaaa` withholds AAAA records from clients when an A record exists. Use only if unavoidable: it can wrongly stop other recursive servers from receiving AAAA.

`synthrecord.so` works only inside a zone clause. In a reverse zone it synthesizes PTR answers from `prefix` and `origin`; in a forward zone it answers A and AAAA for names in `prefix` plus address plus `origin`. Synthesized responses are not signed, so it is incompatible with DNSSEC.

## Checked

2026-11-04. Read the plugin grammar in the Administrator Reference Manual (options, view, zone, template scopes) and the filter-aaaa.so, filter-a.so and synthrecord.so man pages: syntax, example options, the AAAA-filtering warning, zone-clause-only rule for synthrecord and the DNSSEC incompatibility note confirmed. Nothing was removed.

Method: documentation only; no commands were run.
