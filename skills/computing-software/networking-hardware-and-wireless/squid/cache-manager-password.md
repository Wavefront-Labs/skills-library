---
id: computing-software.networking-hardware-and-wireless.squid.cache-manager-password
name: cache-manager-password
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, cachemgr-passwd, cache-manager, admin-actions]
level: practitioner
status: docs-checked
description: "Protect cache manager actions with cachemgr_passwd, including disable all."
sources:
  - https://www.squid-cache.org/Doc/config/cachemgr_passwd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cachemgr_passwd
Default: no password; actions that require a password are denied.
```
cachemgr_passwd secret shutdown
cachemgr_passwd lesssssssecret info stats/objects
cachemgr_passwd disable all
```
One password may cover several actions; `disable all` turns off all cache manager actions.

## Checked

2026-11-04. Read the cachemgr_passwd directive page and confirmed the default, usage, the disable keyword and the three examples. Nothing was removed.

Method: documentation only; no commands were run.
