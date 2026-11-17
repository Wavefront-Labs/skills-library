---
id: computing-software.networking-hardware-and-wireless.squid.store-id-helper
name: store-id-helper
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, store-id, store-id-program, cache-key, helper]
level: advanced
status: docs-checked
description: "Choose the cache key per request with a store_id_program helper so equivalent URLs share one cached object."
sources:
  - https://www.squid-cache.org/Doc/config/store_id_program/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# store_id_program
Specifies the StoreID helper that picks the cache key. No helper is included and none is used by default. It replaces `storeurl_rewrite_program`.

Replies: `OK store-id="..."` uses the supplied ID; `ERR` keeps the request URL as the ID; `BH` is an internal helper error. Supports `concurrency=` channel tags.

`refresh_pattern` applies to the returned StoreID, not the URL. The page warns that a wrong StoreID from a careless helper may return the wrong cached response to the user.

## Checked

2026-11-04. Read the store_id_program directive page and confirmed the replies, the storeurl_rewrite_program replacement, the refresh_pattern note and the helper warning. Reworded the warning to match the page: a wrong StoreID may return the wrong cached response.

Method: documentation only; no commands were run.
