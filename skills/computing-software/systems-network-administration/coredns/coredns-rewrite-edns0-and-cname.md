---
id: computing-software.systems-network-administration.coredns.coredns-rewrite-edns0-and-cname
name: coredns-rewrite-edns0-and-cname
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, rewrite, edns0, cname, ecs]
level: advanced
status: docs-checked
description: "Set, append, replace or unset EDNS0 local, NSID and subnet options and rewrite CNAME targets with the rewrite plugin."
sources:
  - https://coredns.io/plugins/rewrite/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manipulate EDNS0 options and CNAME targets.

EDNS0 actions: `replace` modifies a matching option; `append` adds one only if none matches; `set` modifies or adds; `unset` removes. Supported: EDNS0_LOCAL, EDNS0_NSID, EDNS0_SUBNET.

- LOCAL has `code` and `data`; a match is the same code. Data starting with `0x` is hex. `rewrite edns0 local set 0xffee 0x61626364` equals `... set 0xffee abcd`. Data may be a variable in braces: `{qname}`, `{qtype}`, `{client_ip}`, `{client_port}`, `{protocol}`, `{server_ip}`, `{server_port}`. With the metadata plugin, labels work too; a missing label becomes an empty string. Remove with `rewrite edns0 local unset 0xffee`.
- NSID has no fields and adds an empty NSID option.
- SUBNET takes IPv4 and IPv6 mask lengths: `rewrite edns0 subnet set 24 56` uses the first 24 bits of an IPv4 source and 56 of an IPv6. Remove with `rewrite edns0 subnet unset`.

Add `revert` to drop the change from the response. If only some rules use revert, the response carries the previous value.

CNAME syntax: `rewrite [continue|stop] cname [exact|prefix|suffix|substring|regex] FROM TO`. Records before the CNAME target are kept, the target is rewritten, and later records are replaced with the lookup result, e.g.

`rewrite cname regex (.*).cdn.example.net. {1}.other.cdn.com.`

## Checked

2026-11-08. Checked in full against the rewrite plugin README. EDNS0 actions, variables, subnet, revert and CNAME behaviour match; no changes needed beyond promotion.

Method: documentation only; no commands were run.
