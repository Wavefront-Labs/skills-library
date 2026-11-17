---
id: computing-software.messaging-and-integration.rabbitmq.oauth2-authentication
name: oauth2-authentication
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, oauth2-authentication]
level: advanced
status: docs-checked
description: "Use the OAuth 2 plugin with JWT scopes for the management UI and clients."
sources:
  - https://www.rabbitmq.com/docs/oauth2
  - https://www.rabbitmq.com/docs/management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OAuth 2.0 authentication

**Goal:** Federate login via an identity provider.

## Steps
1. `rabbitmq-plugins enable rabbitmq_auth_backend_oauth2`.
2. Set `auth_oauth2.resource_server_id`. RabbitMQ expects its resource server id in one of the token's audience values.
3. Point RabbitMQ at the provider's signing keys: preferably `auth_oauth2.issuer` (OpenID Connect discovery of the JWKS endpoint), or `auth_oauth2.jwks_uri`, or configure signing keys directly.
4. Scopes map to permissions, for example `rabbitmq.read:*/*` and `rabbitmq.tag:management`.

## Failure modes
- A token whose audience lacks the resource server id is rejected.

## Verify
- Connect with a token and check the resulting permissions.

## Checked

2026-11-02. Confirmed in docs/oauth2 and docs/management: plugin name, resource_server_id and audience rule, issuer/jwks_uri/signing keys options, example scopes. Removed: clock-skew claim (not in pages).
Method: documentation only; no commands were run.
