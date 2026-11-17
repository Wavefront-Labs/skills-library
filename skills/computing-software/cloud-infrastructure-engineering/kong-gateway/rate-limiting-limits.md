---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.rate-limiting-limits
name: rate-limiting-limits
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, rate-limiting, limit-by, error-code, plugins, throttling]
level: practitioner
status: docs-checked
description: "rate-limiting plugin windows and keys: second to year limits, limit_by options, header_name and path, 429 error_code and message, ordering rules and response headers."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/rate-limiting/schema.lua
  - https://developer.konghq.com/plugins/rate-limiting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rate-limiting: limits and keys

Limits (numbers greater than 0, none by default): `second`, `minute`, `hour`, `day`, `month`, `year`. At least one must be set. A longer period cannot have a lower limit than a shorter one.

`limit_by` (default `consumer`): `consumer`, `credential`, `ip`, `service`, `header`, `path`. `header` requires `header_name`; `path` requires `path`. With no auth plugin, the client IP is the identity.

Other defaults:
- `error_code` `429`
- `error_message` `API rate limit exceeded`
- `hide_client_headers` `false`

Docs example config, a per-second limit:

```yaml
config:
  second: 10
```

Response headers: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, plus per-window `X-RateLimit-Limit-<Window>` and `X-RateLimit-Remaining-<Window>`. When exceeded Kong returns `429` with `Retry-After`.

Hide the headers with `hide_client_headers: true`.

For storage and consistency (`policy`, `sync_rate`), see the rate-limiting policy skill.

## Checked

2026-11-04. Confirmed against the rate-limiting schema.lua (limits gt 0, period ordering check, limit_by values, conditional header_name/path, error_code, error_message, hide_client_headers) and the plugin page (client IP as identity without auth, response headers, Retry-After on 429, second: 10 example). Removed the response-ratelimiting pointer: not stated in the cited sources.

Method: documentation only; no commands were run.
