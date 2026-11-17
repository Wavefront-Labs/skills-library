---
id: computing-software.cybersecurity-defensive.keycloak.oidc-token-audience-restriction
name: oidc-token-audience-restriction
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, audience, aud-claim, audience-resolve, token-exchange]
level: practitioner
status: docs-checked
description: "Limit access token audiences so a low-trust service cannot replay a token against other services; use audience resolve, hardcoded audience or token exchange."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/clients/oidc/con-audience.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# oidc token audience restriction
In environments where trust among services is low, an access token valid for several services can be misused: `service1` could replay the token it received from the frontend to call `service2` on the user's behalf. The `aud` claim should typically hold the client ids of all services where the token may be used. The docs recommend limiting the audiences on the token to a minimum and configuring every service to verify the audience.

Ways to get audiences into a token:
- **Audience resolve**: the `Audience Resolve` protocol mapper in the default `roles` client scope adds the client id of each client for which the token has at least one client role available. Useful when service clients rely on client roles.
- **Hardcoded audience**: create a client scope (the docs use `service1-scope`) with an audience mapper; the frontend adds it to the request (`scope=service1-scope`), and the token carries `"aud": "service1"`. With two scopes (`scope=service1-scope service2-scope`) the token is `"aud": [ "service1", "service2" ]`.
- **Token exchange**: if `service1` must call `service2` but the frontend must not call `service2` directly, keep only `service1` in the initial token and let `service1` exchange it for a token with `service2` as audience.

Putting both services in one token means the frontend can also call `service2` directly. Enabling audience checking in the service is done in a way specific to your OIDC adapter.

## Checked
2026-11-03. Confirmed against server_admin/topics/clients/oidc/con-audience.adoc. Removed (not on the page): the "adapters check audience in an adapter-specific way" paraphrase beyond what is stated, the `scope=openid` form of the example, the "no check gains nothing" gotcha and the Verify step.
Method: documentation only; no commands were run.
