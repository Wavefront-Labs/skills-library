---
id: computing-software.systems-network-administration.healthchecks.api-list-checks
name: api-list-checks
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, api-list-checks, tag-filter, unique-key, check-object]
level: practitioner
status: docs-checked
description: "List and fetch checks with the Healthchecks API v3: slug and tag filters, lookup by UUID or unique_key, status values and key check object fields."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List checks: `GET /api/v3/checks/` returns `{"checks": [...]}` (200, 401).
- `slug=<value>`: checks with that slug; empty list if none; all matches if several.
- `tag=<value>`: checks with that tag; repeatable (`?tag=foo&tag=bar`).

Get one check: `GET /api/v3/checks/<uuid>` or `GET /api/v3/checks/<unique_key>` (200, 401, 403, 404). A wrong API key gives 403. Read-only responses omit `uuid` and add `unique_key`, which is stable across calls and can be used instead of the UUID.

Check object fields:
- Core: `name`, `slug`, `tags`, `desc`, `uuid`.
- Timing: `timeout`, `grace`, `schedule`, `tz`, `started`, `last_ping`, `next_ping`, `n_pings`.
- Status: one of `new`, `up`, `grace`, `down`, `paused`.
- Behaviour: `manual_resume`, `methods`.
- Keywords and filters: `start_kw`, `success_kw`, `failure_kw`, `filter_subject`, `filter_body`, `filter_http_body`, `filter_default_fail`.
- URLs: `ping_url`, `update_url`, `pause_url`, `resume_url`, `badge_url`.
- Integrations: `channels` (comma-separated UUIDs).

Example:

```
curl --header "X-Api-Key: <your-api-key>" "<site-root>/api/v3/checks/?tag=prod"
```

## Checked

2026-11-04. Confirmed against the Healthchecks Management API v3 page (templates/docs/api.md): slug and tag query parameters, get-single-check identifiers and response codes, status values, check object fields, read-only field changes. Reworded the read-only unique_key line, which was stated too strongly.

Method: documentation only; no commands were run.
