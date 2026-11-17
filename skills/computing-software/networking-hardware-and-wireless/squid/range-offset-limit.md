---
id: computing-software.networking-hardware-and-wireless.squid.range-offset-limit
name: range-offset-limit
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, range-offset-limit, range-requests, partial-content]
level: advanced
status: docs-checked
description: "Control whether Range requests make Squid fetch whole objects for caching with range_offset_limit."
sources:
  - https://www.squid-cache.org/Doc/config/range_offset_limit/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# range_offset_limit
Syntax: `range_offset_limit (size) [units] [[!]aclname]`. Sets how far into a file a Range request can start and still make Squid prefetch the whole object to cache it. Beyond the limit the request is forwarded unchanged and not cached.

- `0` (default): fetch only what the client requested
- `none`: always fetch from the beginning so it can be cached
- units: bytes if omitted; KB, MB and others accepted

Lines are checked top to bottom; the first matching ACL is used. `none` overrides quick_abort settings, so the full range is fetched regardless of client actions, increasing bandwidth use.

## Checked

2026-11-04. Read the range_offset_limit directive page and confirmed the syntax, 0 and none, the first-match rule and the quick_abort override. Nothing was removed.

Method: documentation only; no commands were run.
