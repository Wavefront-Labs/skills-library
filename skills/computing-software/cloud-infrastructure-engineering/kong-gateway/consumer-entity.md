---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.consumer-entity
name: consumer-entity
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, consumer, custom-id, credentials, admin-api, consumers]
level: intro
status: docs-checked
description: "The Kong Consumer entity: username and custom_id, credentials per auth plugin, plugin scoping limits, centrally managed Consumers, and the Admin API create call."
sources:
  - https://developer.konghq.com/gateway/entities/consumer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer entity

A Consumer identifies an external client (application, service or user). It enables authentication, per-Consumer rate limiting and transformations.

The docs examples set `username` and `custom_id` (an ID from your own system).

Create one:

```bash
curl -i -X POST http://localhost:8001/consumers/ \
  --header "Content-Type: application/json" \
  --data '{"username": "<USERNAME>", "custom_id": "<CUSTOM_ID>"}'
```

Credentials depend on the auth plugin: key-auth uses an API key, basic-auth a username and password pair. Credential endpoints live under the Consumer, for example `/consumers/{usernameOrId}/key-auth`.

Scoping rules:
- Most plugins can be scoped to a Consumer, except authentication and routing plugins.
- Authentication plugins must be scoped to a Route, a Service, or globally.

For many Consumers, group them with Consumer Groups.

Centrally managed Consumers (v3.10+) are managed through the Konnect Consumers API, must belong to a realm, support only Key Auth, and cannot have plugins scoped directly to them.

## Checked

2026-11-04. Confirmed against the Consumers page: purpose, credentials per auth plugin, plugin scoping exceptions (authentication and routing plugins), Consumer Groups for decK at scale, and the centrally managed Consumer table. Removed the field list, username and custom_id uniqueness and the at-least-one-of rule: the page's schema section is empty.

Method: documentation only; no commands were run.
