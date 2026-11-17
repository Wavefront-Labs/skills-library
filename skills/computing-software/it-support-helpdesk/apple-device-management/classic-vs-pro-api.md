---
id: computing-software.it-support-helpdesk.apple-device-management.classic-vs-pro-api
name: classic-vs-pro-api
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-api, classic-vs-pro-api, classic-api, pro-api]
level: practitioner
status: draft
description: "Choose between the Jamf Classic API (XML or JSON, resource-based) and the newer Jamf Pro API (JSON, OpenAPI) and plan migration as Classic is retired."
sources:
  - "https://developer.jamf.com/jamf-pro/docs/jamf-pro-api-overview"
  - "https://developer.jamf.com/jamf-pro/reference"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# classic-vs-pro-api

Goal: pick the right API for new automation.
- Classic: `/JSSResource/...`, XML by default, basic auth or bearer; still used for many writes.
- Pro API: `/api/v1/...` and `/api/v2/...`, JSON, OpenAPI docs at `<server>/api`.
- Get a bearer token: `POST /api/v1/auth/token` with basic auth; Classic also accepts the token.
- Prefer Pro API endpoints where available; Classic deprecations are announced in release notes (confirm).
- Use pagination parameters `page`, `page-size`, `sort`, and `filter`.
Practice: Log which endpoints your scripts use and check each Jamf release note for deprecations, so you can schedule the move to Pro API endpoints before Classic ones are removed.
Gotcha: the two APIs expose different field names for the same data; do not assume ids match between Classic computer ids and Pro inventory ids without checking.
Verify:
- Token request returns a token and expiry.
- A GET on `/api/v1/jamf-pro-version` returns the version.
