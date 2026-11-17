---
id: computing-software.networking-hardware-and-wireless.squid.refresh-pattern
name: refresh-pattern
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, refresh-pattern, freshness, min-percent-max, override-expire, ignore-reload]
level: practitioner
status: draft
description: "Control cached-object freshness with refresh_pattern: min, percent, max and the override options."
sources:
  - https://www.squid-cache.org/Doc/config/refresh_pattern/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# refresh_pattern
Syntax: `refresh_pattern [-i] regex min percent max [options]`. First matching entry wins; `-i` makes the regex case-insensitive.

- min: minutes of freshness for objects without explicit expiry (0 recommended)
- percent: share of the age since Last-Modified used to compute freshness
- max: upper freshness limit; also used for the max-age on requests to origins or parents

Options: `override-expire`, `override-lastmod`, `reload-into-ims`, `ignore-reload`, `ignore-no-store`, `ignore-private` (all violate HTTP), `refresh-ims`, `store-stale`, `max-stale=NN`. The page warns that overriding may create liability.

Defaults:
```
refresh_pattern ^ftp:		1440	20%	10080
refresh_pattern -i (/cgi-bin/|\?) 0	0%	0
refresh_pattern .		0	20%	4320
```
