---
id: computing-software.networking-hardware-and-wireless.squid.cache-allow-deny
name: cache-allow-deny
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, cache-directive, no-cache, send-hit, store-miss]
level: practitioner
status: docs-checked
description: "Exclude requests from the cache with the cache directive, plus send_hit and store_miss."
sources:
  - https://www.squid-cache.org/Doc/config/cache/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cache, send_hit, store_miss
`cache` replaces `no_cache` and is unused by default. When its ACL matches with deny, Squid neither serves the request from cache nor stores the response. Supports fast and slow ACL types.

- `send_hit`: deny serving a hit; fast ACLs only
- `store_miss`: deny storing a miss; fast ACLs only

The directive has no effect on other transactions or on already cached responses.

## Checked

2026-11-04. Read the cache directive page and confirmed the no_cache replacement, the default, the fast and slow ACL support of cache, send_hit and store_miss and the no-effect note. Nothing was removed.

Method: documentation only; no commands were run.
