---
id: computing-software.systems-network-administration.healthchecks.api-pings-flips
name: api-pings-flips
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, api-pings-log, api-flips, status-changes, ping-body-api]
level: advanced
status: docs-checked
description: "Read a Healthchecks check's logged pings, ping bodies and status changes (flips) through API v3, with limits, time filters and retention."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pings: `GET /api/v3/checks/<uuid>/pings/`, most recent first. The result limit is 100 on free accounts and 1000 on paid ones. Ping fields: `type` (for example `success`, `start`), `date`, `n`, `scheme`, `remote_addr`, `method`, `ua`, `rid`, `duration`, `body_url`.

Ping body: `GET /api/v3/checks/<uuid>/pings/<n>/body` returns the body verbatim as `text/plain`. 404 if the check or ping is missing or has no body; 503 if external object storage is unavailable (retry later).

Flips (status changes): `GET /api/v3/checks/<uuid>/flips/` or with `<unique_key>`.
- `seconds=<value>`: flips from the last N seconds.
- `start=<value>` and `end=<value>`: UNIX timestamps bounding newer and older flips.
- No filters returns all stored flips.
- Response: array of `{timestamp, up (1 or 0)}`.
- Retention: current month plus the two full months before; older flips are cleaned periodically, so some may still appear.
- 400 for invalid query parameters.

## Checked

2026-11-04. Confirmed against the Healthchecks Management API v3 page (templates/docs/api.md): pings list order and plan limits of 100 and 1000, ping fields, ping body behaviour and 404 or 503 cases, flips time filters, retention note, 400 on invalid parameters. Removed: the ISO 8601 label and the closing usage advice, which the page does not state.

Method: documentation only; no commands were run.
