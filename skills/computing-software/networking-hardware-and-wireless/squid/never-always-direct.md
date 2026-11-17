---
id: computing-software.networking-hardware-and-wireless.squid.never-always-direct
name: never-always-direct
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, never-direct, always-direct, forwarding, cache-peer]
level: practitioner
status: docs-checked
description: "Force requests through peers with never_direct or keep them off peers with always_direct."
sources:
  - https://www.squid-cache.org/Doc/config/never_direct/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# never_direct and always_direct
`never_direct allow|deny [!]aclname ...` lists requests that must never go straight to origin servers, so they go via a peer. `always_direct` is the opposite: requests that always bypass peers.

Docs example, forcing proxy use for everything except local-domain traffic:
```
never_direct deny local-servers
never_direct allow all
```

## Checked

2026-11-04. Read the never_direct directive page and confirmed the syntax, the opposite-of-always_direct description and the local-domain example. Nothing was removed.

Method: documentation only; no commands were run.
