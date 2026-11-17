---
id: computing-software.networking-hardware-and-wireless.squid.http-access-rule-order
name: http-access-rule-order
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, http-access, allow-deny, rule-order, access-control]
level: intro
status: draft
description: "Control who may use the proxy with http_access: syntax, first-match order and the implicit default when no line matches."
sources:
  - https://www.squid-cache.org/Doc/config/http_access/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# http_access rule order
Syntax: `http_access allow|deny [!]aclname ...`. It applies to requests on HTTP, HTTPS and FTP ports and supports fast and slow ACL types.

Behaviour:
- Lines are checked in the order they appear in squid.conf.
- With no access lines at all, requests are denied.
- If no line matches, the result is the reverse of the last line's action: a final deny yields allow, a final allow yields deny.
- End the list with a catch-all rule to avoid confusion.

Lines from the suggested configuration:
```
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access allow localhost manager
http_access deny manager
http_access allow localhost
http_access deny all
```
