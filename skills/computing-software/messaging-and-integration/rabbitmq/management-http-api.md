---
id: computing-software.messaging-and-integration.rabbitmq.management-http-api
name: management-http-api
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, management-http-api]
level: practitioner
status: docs-checked
description: "Automate with the HTTP API under /api, including definitions, queues and healthchecks."
sources:
  - https://www.rabbitmq.com/docs/http-api-reference
  - https://www.rabbitmq.com/docs/management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Management HTTP API

**Goal:** Script operations without rabbitmqctl.

## Steps
1. `curl -u user:PASS https://host:15671/api/overview` (15671 is the management TLS port in the guide's examples).
2. Endpoints: `/api/queues/{vhost}`, `/api/definitions`, `/api/health/checks/...`.
3. The default vhost `/` must be encoded as `%2F` in paths.
4. `rabbitmqadmin` v2 is a command-line tool for the HTTP API.

## Failure modes
- Vhost names in paths must be URL-encoded.

## Verify
- `GET /api/health/checks/alarms` returns 200 OK when no alarms are in effect, otherwise 503.

## Checked

Date: 2026-11-02. Confirmed on the HTTP API reference and Management guide. Removed: Terraform recommendation, "forgetting %2F returns 404".

Method: documentation only; no commands were run.
