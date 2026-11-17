---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.irules-data-groups
name: irules-data-groups
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, data-groups, class-match, address-lists]
level: practitioner
status: draft
description: "Use BIG-IP data groups for IP allow lists, URI maps and lookups from iRules with class match and class lookups."
sources:
  - https://clouddocs.f5.com/api/irules/class.html
  - https://clouddocs.f5.com/api/irules/HTTP__header.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data groups (classes) in iRules

```
tmsh create ltm data-group internal dg_allow type ip records add { 10.1.0.0/16 { } 192.0.2.7/32 { } }
tmsh create ltm data-group internal dg_uri type string records add { "/shop" { data pool_shop } "/blog" { data pool_blog } }
tmsh create ltm data-group external dg_ext type string source-path file:/var/tmp/uris.txt
tmsh list ltm data-group internal dg_uri
```
```
when CLIENT_ACCEPTED {
  if { not [class match [IP::client_addr] equals dg_allow] } { reject }
}
when HTTP_REQUEST {
  set p [class match -value [HTTP::path] starts_with dg_uri]
  if { $p ne "" } { pool $p }
}
```
- Types are `string`, `address` (`ip`) and `integer`. The match operators: `equals`, `starts_with`, `ends_with`, `contains`, `matches_regex` and `all`. `class match` returns a boolean; `class lookup` returns the value; `class search` iterates.
- Internal data groups live in `bigip.conf` and sync; large ones (thousands) are slow to load. Use external files (`/var/tmp`, `tmsh create sys file data-group`) for big lists, edited and re-loaded.
- Address data groups are searched by longest prefix, so overlaps resolve as expected.
- Gotcha: with route domains, `IP::client_addr` has a `%id` suffix and does not match; mask or strip first.
- Updating a data group takes effect immediately for new `class match` calls without touching the rule.

Verify: `tmsh list ltm data-group`, then a test `curl` from an allowed and a blocked source, and `tmsh show ltm rule` for `Aborts`.
