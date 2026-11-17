---
id: computing-software.networking-hardware-and-wireless.squid.cache-peer-access-control
name: cache-peer-access-control
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, cache-peer-access, peer-selection, acl]
level: practitioner
status: docs-checked
description: "Limit which requests may use a given cache_peer with cache_peer_access allow and deny rules."
sources:
  - https://www.squid-cache.org/Doc/config/cache_peer_access/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache_peer_access
Syntax: `cache_peer_access peer-name allow|deny [!]aclname ...`.

- A matching deny stops Squid sending ICP queries or HTTP requests to that peer.
- For each peer the first matching rule takes effect, so group rules per peer.
- It narrows candidates; it does not set contact order (peer selection algorithms do).
- Only fast ACL types are supported.
- Default: no restrictions.

## Checked

2026-11-04. Read the cache_peer_access directive page and confirmed the syntax, deny and allow behaviour, first match per peer, ordering note and default. Nothing was removed.

Method: documentation only; no commands were run.
