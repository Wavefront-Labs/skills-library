---
id: computing-software.systems-network-administration.healthchecks.filtering-http-methods
name: filtering-http-methods
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, allowed-methods, post-only, sticky-paused, manual-resume]
level: practitioner
status: docs-checked
description: "Restrict a Healthchecks check to POST pings to stop link-preview bots causing false signals, and make the paused state sticky with manual resume."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/configuring_checks.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Filtering rules control how incoming pings are handled.

Allowed HTTP methods: you can require POST. This helps when chat or email preview bots fetch a ping URL (for instance after it is pasted into a chat) and cause false signals. API field `methods`: `""` allows HEAD, GET and POST; `"POST"` allows only POST.

Paused checks: by default a ping to a paused check resumes it, moving it to up or down depending on the signal. You can make the paused state sticky, so pings are ignored until you resume manually. API field `manual_resume` (boolean, default false).

API calls:
- `POST /api/v3/checks/<uuid>/pause` pauses a check. Unless `manual_resume` is true, a ping resumes it.
- `POST /api/v3/checks/<uuid>/resume` moves it to `new`; it returns 409 if the check is not paused. Intended mainly for `manual_resume` checks.

## Checked

2026-11-04: confirmed against the Configuring Checks page (Only POST option, sticky paused state) and the Management API page (methods, manual_resume default false, pause and resume calls, resume 409 when not paused). Removed an unsourced maintenance recommendation.
Method: documentation only; no commands were run.
