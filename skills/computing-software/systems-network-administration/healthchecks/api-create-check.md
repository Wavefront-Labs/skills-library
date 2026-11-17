---
id: computing-software.systems-network-administration.healthchecks.api-create-check
name: api-create-check
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, api-create-check, unique-upsert, check-parameters, channels-parameter]
level: advanced
status: docs-checked
description: "Create Healthchecks checks with POST /api/v3/checks/: parameters, schedule kinds, the unique upsert, channels assignment and the 201, 200 and 403 outcomes."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`POST /api/v3/checks/` (201, 200, 400, 401, 403). All parameters are optional; omitted ones take defaults. The response includes `ping_url`.

Parameters:
- `name`, `slug` (max 100 characters each; slug uses a-z, 0-9, hyphen, underscore), `tags` (space-delimited), `desc` (max 10,000 characters).
- Simple check: `timeout` and `grace`, 60 to 31536000 seconds.
- Cron or OnCalendar: `schedule` and `tz` (default `UTC`). `schedule` overrides `timeout`.
- `manual_resume` (default false), `methods` (`""` or `"POST"`).
- `channels`: `"*"` for all integrations, or UUIDs or exact names, comma-separated. Nothing is assigned if omitted.
- Keyword fields: `start_kw`, `success_kw`, `failure_kw`, `filter_subject`, `filter_body`, `filter_http_body`, `filter_default_fail`.
- `unique` (create only): array of fields (`name`, `slug`, `tags`, `timeout`, `grace`) to match on. An existing match is updated and returns 200; otherwise 201.

Idempotent provisioning:

```
{"name": "Backups", "unique": ["name"]}
```

403 means the check limit was reached (free accounts: 20).

## Checked

2026-11-04. Confirmed against the Healthchecks Management API v3 page (templates/docs/api.md): status codes, field length limits, timeout and grace range, schedule precedence over timeout, tz default, channels values, unique accepted fields and 201 or 200 outcomes, free-account limit of 20 checks. Nothing removed.

Method: documentation only; no commands were run.
