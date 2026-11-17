---
id: computing-software.collaboration-platform-administration.vikunja.webhooks-api-and-signature
name: webhooks-api-and-signature
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, webhook-endpoints, webhook-payload, hmac-signature, webhook-delivery]
level: practitioner
status: docs-checked
description: "Create Vikunja webhooks via the API, read the event payload, verify the X-Vikunja-Signature HMAC, and know delivery, timeout and SSRF behaviour."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/integrations/webhooks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Endpoints (API token or JWT; link share tokens cannot manage webhooks):
- Project: `GET|PUT /api/v1/projects/{id}/webhooks`, `POST|DELETE /api/v1/projects/{id}/webhooks/{webhookID}` (POST updates).
- User: `GET|PUT /api/v1/user/settings/webhooks`, `POST|DELETE .../{webhookID}`.

Each delivery is a POST with JSON `{"event_name": "task.created", "time": ISO8601, "data": {...}}`. Task events carry the task and the `doer`; comment, attachment and relation events carry the sub-object.

Signing: with a secret set, Vikunja sends `X-Vikunja-Signature`, the HMAC-SHA256 of the raw body keyed by the secret. Verify against the raw bytes before parsing JSON.

Delivery: once only. Status >= 400 or timeout is not retried. Default timeout 30 seconds (`webhooks.timeoutseconds`). `webhooks.enabled` is on by default.

SSRF: by default private, loopback and link-local targets are refused, so a receiver on your LAN will not get calls. For multi-user instances route egress through a proxy such as mole via `outgoingrequests.proxyurl` and `proxypassword` (the deprecated `webhooks.proxyurl` and `webhooks.proxypassword` still work).

## Checked

2026-11-04. Confirmed against the Vikunja Webhooks API page (integrations/webhooks): project and user endpoints, authentication and link share limit, payload fields, signature header and verification steps, SSRF default and proxy settings, delivery behaviour, default timeout and webhooks.enabled. Removed: the constant-time comparison advice, which the page does not state.

Method: documentation only; no commands were run.
