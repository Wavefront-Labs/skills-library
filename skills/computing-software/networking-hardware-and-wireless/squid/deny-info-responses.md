---
id: computing-software.networking-hardware-and-wireless.squid.deny-info-responses
name: deny-info-responses
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, deny-info, error-page, redirect, tcp-reset]
level: practitioner
status: draft
description: "Customise the reply to a denied request with deny_info: error pages, redirect URLs, status codes and TCP_RESET."
sources:
  - https://www.squid-cache.org/Doc/config/deny_info/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# deny_info
Returns a custom response when a request fails `http_access`. Default none.

- Error page: `deny_info ERR_CUSTOM_ACCESS_DENIED bad_guys`
- Redirect: a URL such as `303:http://example.com/`
- Reset: `deny_info TCP_RESET acl`

Without a status prefix Squid sends 403; set another 4xx or 5xx, for example `404:ERR_CUSTOM_ACCESS_DENIED`. Redirect URLs accept tags such as `%i` (client IP), `%M` (method) and `%w` (admin email).
