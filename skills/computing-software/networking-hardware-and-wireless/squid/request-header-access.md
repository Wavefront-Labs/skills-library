---
id: computing-software.networking-hardware-and-wireless.squid.request-header-access
name: request-header-access
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, request-header-access, header-filtering, via, anonymity]
level: advanced
status: docs-checked
description: "Strip or allow outgoing request headers with request_header_access, and toggle the Via header with via."
sources:
  - https://www.squid-cache.org/Doc/config/request_header_access/
  - https://www.squid-cache.org/Doc/config/via/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Header filtering
`request_header_access header_name allow|deny [!]aclname ...`. Header name: a field such as `From`, `Other` (names not on Squid's hard-coded list), or `All`. For each header the first match is taken in order: named header, `Other`, `All`. An allow match passes it; a deny match removes it and `request_header_replace` is checked; no match leaves it. `reply_header_access` does the same for replies. Needs `--enable-http-violations`.
```
request_header_access From deny all
request_header_access Referer deny all
request_header_access User-Agent deny all
```
`via` (default on) adds Via headers as RFC2616 requires; it also needs `--enable-http-violations`.

## Checked

2026-11-04. Read the request_header_access and via directive pages and confirmed the syntax, build option, Other and All rule order, deny and request_header_replace behaviour, the example and the via default. Nothing was removed.

Method: documentation only; no commands were run.
