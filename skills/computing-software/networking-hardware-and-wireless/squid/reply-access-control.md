---
id: computing-software.networking-hardware-and-wireless.squid.reply-access-control
name: reply-access-control
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, http-reply-access, reply, access-control]
level: practitioner
status: draft
description: "Filter replies going back to clients with http_reply_access, which complements http_access."
sources:
  - https://www.squid-cache.org/Doc/config/http_reply_access/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reply access control
`http_reply_access allow|deny [!] aclname ...` controls replies to client requests.

- Default: allow, unless rules exist in squid.conf. With no access lines all replies are allowed.
- If no line matches, the opposite of the last line applies, so end with an `allow all` or `deny all` entry.
- Supports fast and slow ACL types.
- It complements `http_access`, which decides on the request.
