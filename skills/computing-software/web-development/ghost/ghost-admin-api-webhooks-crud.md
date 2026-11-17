---
id: computing-software.web-development.ghost.ghost-admin-api-webhooks-crud
name: ghost-admin-api-webhooks-crud
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, webhooks, integration-id, secret, target-url]
level: practitioner
status: docs-checked
description: "Create, update and delete Ghost webhooks via the Admin API with event, target_url, secret and integration_id rules."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api/webhooks/creating-a-webhook.mdx
  - https://github.com/TryGhost/docs/blob/main/admin-api/webhooks/overview.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: register webhooks from code instead of Ghost Admin.

Create: `POST /admin/webhooks/`. Required: `event` and `target_url`. Optional: `name`, `secret`, `api_version`. Conditionally required: `integration_id`, needed when the request uses user authentication (with token authentication the integration is implied).

Example (token auth): `{"webhooks":[{"event":"post.added","target_url":"https://example.com/hook/","secret":"<SHARED_SECRET>"}]}`.

Update with `PUT /admin/webhooks/{id}/` and remove with `DELETE /admin/webhooks/{id}/`. There is no API to retrieve webhook resources independently. Event names and delivery rules: see ghost-webhook-events-and-delivery.

Verify: trigger the event in Ghost and confirm your endpoint receives the HTTP POST payload.

## Checked

2026-11-04. Confirmed: POST path, required event and target_url, optional name, secret and api_version, conditional integration_id, update and delete paths, no retrieve API, HTTP POST on events (creating a webhook and webhooks overview pages). Removed: the 2xx receiver contract, the "reachable from the Internet" and one-webhook-per-event tips, the operational notes and the event name post.published, none shown on these pages.

Method: documentation only; no commands were run.
