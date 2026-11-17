---
id: computing-software.networking-hardware-and-wireless.squid.url-rewrite-helper
name: url-rewrite-helper
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, url-rewrite-program, redirector, helper, rewrite-url]
level: advanced
status: docs-checked
description: "Redirect or rewrite request URLs with a url_rewrite_program helper and its OK, ERR and BH replies."
sources:
  - https://www.squid-cache.org/Doc/config/url_rewrite_program/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# url_rewrite_program
Squid sends one line per request: `[channel-ID] request-URL [extras]` (control extras with `url_rewrite_extras`). It replaces `redirect_program`. The helper runs after `http_access` and eCAP/ICAP adaptation, and before `adapted_http_access`.

Replies:
- `OK url="..."`: redirect the client; optional `status` of 301, 302 (default), 303, 307 or 308
- `OK rewrite-url="..."`: silently replace the URL; the page warns to avoid rewriting, since Location headers and embedded URLs are not adjusted
- `OK` or `ERR`: no change
- `BH message="..."`: helper fault, logged at level 1

Channel-IDs appear only when `url_rewrite_children` sets positive concurrency (IDs 0 to concurrency-1, echoed back by the helper).

## Checked

2026-11-04. Read the url_rewrite_program directive page and confirmed the line formats, the OK, ERR and BH replies, status codes, the rewrite warning, the redirect_program replacement and the channel-ID rule. Nothing was removed.

Method: documentation only; no commands were run.
