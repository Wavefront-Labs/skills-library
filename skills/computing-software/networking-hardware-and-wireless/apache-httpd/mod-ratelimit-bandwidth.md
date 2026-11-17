---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-ratelimit-bandwidth
name: mod-ratelimit-bandwidth
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-ratelimit, bandwidth, throttling, rate-limit, output-filter]
level: intro
status: docs-checked
description: "Throttle download bandwidth per response with mod_ratelimit: the RATE_LIMIT filter, rate-limit and rate-initial-burst variables and the worker-cost warning."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_ratelimit.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_ratelimit
Filter `RATE_LIMIT` limits bandwidth per HTTP response, not per IP or client.

```apache
<Location "/downloads">
    SetOutputFilter RATE_LIMIT
    SetEnv rate-limit 400
    SetEnv rate-initial-burst 512
</Location>
```
- `rate-limit`: simulated connection speed in KiB/s.
- `rate-initial-burst`: KiB sent at full speed before throttling (2.4.24+).

Here `/downloads` runs at 400 KiB/s after the first 512 KiB.

## Cost
Throttling sleeps between writes, so each limited response occupies a worker for the whole transfer. Size `MaxRequestWorkers` accordingly.

## Checked
2026-11-04. Confirmed against the mod_ratelimit reference: per-response limiting, rate-limit and rate-initial-burst in KiB, 2.4.24 compatibility note, example configuration, resource consumption and MaxRequestWorkers advice. Nothing removed.
Method: documentation only; no commands were run.
