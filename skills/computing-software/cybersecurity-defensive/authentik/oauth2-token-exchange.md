---
id: computing-software.cybersecurity-defensive.authentik.oauth2-token-exchange
name: oauth2-token-exchange
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, token-exchange, rfc8693, on-behalf-of, delegation, impersonation]
level: advanced
status: docs-checked
description: "Configure authentik OAuth2 token exchange (RFC 8693): impersonation, on-behalf-of delegation with actor tokens, audience trust and error codes."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/oauth2/token_exchange/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: swap a token you hold for a new one issued by an authentik provider.

## Configure
1. Edit the exchanging provider; under **Grant Types** select `Token exchange` (this also enables delegation); it must be bound to an application.
2. Expand **Machine-to-Machine authentication settings** and add the issuer of subject tokens to **Federated OAuth2/OpenID Providers** or **Federated OIDC Sources**.
3. For an OAuth/JWT actor token, add its issuing provider to Federated OAuth2/OpenID Providers (actor tokens cannot use OIDC sources).
4. To target another provider with `audience`, edit the target provider and add the exchanging provider to its Federated OAuth2/OpenID Providers.
Confidential clients still authenticate; the subject token does not replace credentials.

## Impersonation request
```http
POST /application/o/token/ HTTP/1.1
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange&
client_id=application_client_id&client_secret=application_client_secret&
subject_token=token_issued_by_the_federated_provider&
subject_token_type=urn:ietf:params:oauth:token-type:access_token&
scope=openid email
```
Response: `access_token`, `issued_token_type`, `token_type` (always Bearer), `expires_in`, `scope`. If `scope` is omitted the token has no scopes.

## Delegation (OBO, 2026.8)
Add `actor_token` and `actor_token_type` together (one without the other gives `invalid_request`). `actor_token_type` may be the access_token or jwt URN, or `goauthentik.io/oauth/token-type/authentik_token` for an authentik API token. The actor must be an authentik Actor; a parent user must equal the subject token's user; a parentless Actor works only with an OAuth/JWT token. The issued JWT gets `"act": {"sub": "actor_identifier"}`.

## Audience and errors
`audience` is one provider `client_id` or application `pbm_uuid`; the target's signing key, issuer, subject mode and scope mappings apply, and the target must trust the exchanger and be bound to an application. `resource` is rejected with `invalid_target`. A user failing the target application's policy bindings, or an unverifiable actor token, gives `invalid_grant`. Unsupported token types give `invalid_request`.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/oauth2/token_exchange/.
Removed as not confirmed by that page: SAML response exchange section.
Method: documentation only; no commands were run.
