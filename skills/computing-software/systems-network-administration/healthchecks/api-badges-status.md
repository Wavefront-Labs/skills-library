---
id: computing-software.systems-network-administration.healthchecks.api-badges-status
name: api-badges-status
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, api-badges, api-channels, status-endpoint, shields-json]
level: practitioner
status: docs-checked
description: "Use the Healthchecks API v3 endpoints for integrations, badge URLs per tag and the database status check for external monitoring."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
List integrations: `GET /api/v3/channels/` returns `{"channels": [...]}` with `id`, `name` and `kind` (such as `email`, `sms`). Use these ids or names in a check's `channels` field.

List badges: `GET /api/v3/badges/` (200, 401). Response: `{"badges": {<tag>: {svg, svg3, json, json3, shields, shields3}}}`.
- Formats: `svg`, `json` (to build a custom badge) and `shields` (Shields.io compatible).
- 2-state variants report up and down (checks in grace count as up). 3-state variants (`svg3`, `json3`, `shields3`) report up, late and down.
- The special `*` tag is the overall status of all checks in the project.

Status: `GET /api/v3/status/` runs a test database query. 200 if it succeeded, 500 if it failed. Intended for external uptime monitoring of the Healthchecks instance itself.

Example:

```
curl --header "X-Api-Key: <read-only-key>" <site-root>/api/v3/badges/
```

Read-only keys work with list badges.

## Checked

2026-11-04. Confirmed against the Healthchecks Management API v3 page (templates/docs/api.md): list integrations response fields, list badges formats, 2-state and 3-state variants, the * pseudo-tag, status endpoint 200 and 500 codes and its monitoring purpose, read-only key access to list badges. Nothing removed.

Method: documentation only; no commands were run.
