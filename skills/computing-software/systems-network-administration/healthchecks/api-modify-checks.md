---
id: computing-software.systems-network-administration.healthchecks.api-modify-checks
name: api-modify-checks
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, api-update-check, api-pause-check, api-resume-check, api-delete-check]
level: practitioner
status: docs-checked
description: "Update, pause, resume and delete Healthchecks checks through API v3, with response codes and the manual_resume interaction."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Update: `POST /api/v3/checks/<uuid>` (200, 400, 401, 403, 404). Parameters match create (except `unique`); omitted fields keep current values. `channels` also accepts `""` to unassign all integrations.

```
{"timeout": 300}
```

Pause: `POST /api/v3/checks/<uuid>/pause` (200, 401, 403, 404). No parameters. The check becomes `paused` and resumes when pinged, unless `manual_resume` is true.

Resume: `POST /api/v3/checks/<uuid>/resume` (200, 401, 403, 404, 409). No parameters. The check moves to `new`. Intended mainly for paused checks with `manual_resume=True`; 409 if the check is not paused.

Delete: `DELETE /api/v3/checks/<uuid>` (200, 401, 403, 404). Permanent; returns the deleted check's JSON.

Example:

```
curl -X POST --header "X-Api-Key: <your-api-key>" --data "" <site-root>/api/v3/checks/<uuid>/pause
```

POST bodies must be JSON. A read-only key works only with the list, get, flips and badges endpoints, so these calls need a read-write key.

## Checked

2026-11-04. Confirmed against the Healthchecks Management API v3 page (templates/docs/api.md): update, pause, resume and delete endpoints, response codes, channels empty-string unassign, manual_resume behaviour, 409 on resume when not paused, delete returning the check JSON. Reworded the key-scope line to follow the page.

Method: documentation only; no commands were run.
