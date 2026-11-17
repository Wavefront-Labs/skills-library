---
id: computing-software.networking-hardware-and-wireless.squid.cache-peer-hierarchy
name: cache-peer-hierarchy
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, cache-peer, parent, sibling, round-robin, carp]
level: practitioner
status: docs-checked
description: "Define parent, sibling and multicast neighbours with cache_peer and its selection, ICP and login options."
sources:
  - https://www.squid-cache.org/Doc/config/cache_peer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache_peer hierarchy
Syntax: `cache_peer hostname type http-port icp-port [options]`. Types: `parent`, `sibling`, `multicast`. Set icp-port to 0 if the peer supports neither ICP nor HTCP.

Options:
- ICP/HTCP: `no-query`, `multicast-responder`, `closest-only`, `background-ping`, `htcp`
- selection: `default`, `round-robin`, `weighted-round-robin`, `carp`, `userhash`, `sourcehash`, `weight=N`
- accelerator: `originserver`, `forceddomain=`, `no-digest`
- auth: `login=user:password`, `PASSTHRU`, `PASS`, `*:password`, `NEGOTIATE`
- TLS: `tls`, `sslcert=`, `sslkey=`, `tls-min-version=`, `tls-cafile=`, `ssldomain=`
- general: `name=`, `connect-timeout=`, `proxy-only`, `max-conn=`, `standby=`

Examples from the docs:
```
cache_peer parent.foo.net       parent    3128  3130  default
cache_peer sib1.foo.net         sibling   3128  3130  proxy-only
```

## Checked

2026-11-04. Read the cache_peer directive page and confirmed the syntax, peer types, icp-port 0 rule, the listed ICP, HTCP, selection, accelerator, login, TLS and general options and both examples. Nothing was removed.

Method: documentation only; no commands were run.
