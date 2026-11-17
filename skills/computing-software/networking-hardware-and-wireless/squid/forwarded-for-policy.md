---
id: computing-software.networking-hardware-and-wireless.squid.forwarded-for-policy
name: forwarded-for-policy
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, forwarded-for, x-forwarded-for, privacy, header]
level: intro
status: docs-checked
description: "Choose what Squid puts in outgoing X-Forwarded-For headers with forwarded_for on, off, transparent, delete or truncate."
sources:
  - https://www.squid-cache.org/Doc/config/forwarded_for/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forwarded_for
Controls the X-Forwarded-For header Squid adds to forwarded requests. Default `on`.

- `on`: append the client IP
- `off`: set the value to unknown
- `transparent`: leave the header unchanged
- `delete`: remove the whole header
- `truncate`: remove existing entries and set the client IP as the only one

## Checked

2026-11-04. Read the forwarded_for directive page and confirmed the default and the on, off, transparent, delete and truncate behaviours. Nothing was removed.

Method: documentation only; no commands were run.
