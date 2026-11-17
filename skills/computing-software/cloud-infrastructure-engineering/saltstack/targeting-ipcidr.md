---
id: computing-software.cloud-infrastructure-engineering.saltstack.targeting-ipcidr
name: targeting-ipcidr
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, targeting, ipcidr, subnet, cidr, ipv6]
level: intro
status: docs-checked
description: "Target Salt minions by IP address or CIDR subnet with -S, IPv6 support, compound combination and match: ipcidr in top files."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/targeting/ipcidr.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeting by IP or subnet

`-S` matches a minion by IP address or a CIDR range, IPv4 or IPv6.

```
salt -S 192.168.40.20 test.version
salt -S 2001:db8::/64 test.version
```

Combine with other matchers using `-C` and the `S@` prefix:

```
salt -C 'S@10.0.0.0/24 and G@os:Debian' test.version
```

In a (pillar) top file, key the entry by the CIDR range and set `match: ipcidr`; the page's example assigns an item named `internal` to `172.16.0.0/12`.

## Checked

2026-11-04: read the Salt subnet/IP matching page in full. Confirmed -S with an IPv4 address and an IPv6 CIDR, the compound S@ example and the match: ipcidr entry. Nothing removed.

Method: documentation only; no commands were run.

