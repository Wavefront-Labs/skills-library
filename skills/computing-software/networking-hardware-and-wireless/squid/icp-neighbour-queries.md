---
id: computing-software.networking-hardware-and-wireless.squid.icp-neighbour-queries
name: icp-neighbour-queries
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, icp-port, icp, htcp, neighbour-caches]
level: advanced
status: docs-checked
description: "Enable ICP so Squid exchanges queries with neighbour caches, using icp_port together with cache_peer."
sources:
  - https://www.squid-cache.org/Doc/config/icp_port/
  - https://www.squid-cache.org/Doc/config/cache_peer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ICP queries
`icp_port` sets the port on which Squid sends and receives ICP queries to and from neighbour caches. It replaces `udp_port`. Default: ICP disabled. The standard UDP port is 3130:
```
icp_port 3130
```
On `cache_peer` lines, the icp-port field is the peer's ICP port (0 if unsupported), and `no-query` disables queries to that peer. HTCP peers need `htcp_port` and `htcp_access`; ICP peers need `icp_access`.

## Checked

2026-11-04. Read the icp_port directive page and the cache_peer page and confirmed the default, the udp_port replacement, port 3130, no-query and the icp_access and htcp requirements. Nothing was removed.

Method: documentation only; no commands were run.
