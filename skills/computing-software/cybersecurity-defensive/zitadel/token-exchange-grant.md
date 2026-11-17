---
id: computing-software.cybersecurity-defensive.zitadel.token-exchange-grant
name: token-exchange-grant
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, token-exchange, rfc8693, impersonation, delegation, audience]
level: advanced
status: docs-checked
description: "Know when to use ZITADEL's RFC 8693 token exchange grant to change audience, scope or subject, and how it affects the act claim."
sources:
  - https://zitadel.com/docs/apis/openidoauth/endpoints
  - https://zitadel.com/docs/apis/openidoauth/claims
  - https://zitadel.com/docs/guides/manage/console/administrators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The token exchange grant implements RFC 8693 and swaps one token for another with a different scope, audience or subject. Changing the subject of an authenticated token is called impersonation or delegation. ZITADEL documents token exchange as a separate guide, and the token endpoint lists it among its grants.

Client authentication on the exchange request follows the same options as other token calls: a client secret in a Basic header, `client_id` and `client_secret` in the body, `client_id` alone (no authentication), or a `client_assertion` JWT (private key JWT).

Claims: the `act` claim appears after a token exchange that includes an `actor_token`. It is present in the ID token and introspection response, and in the access token when that is a JWT. It does not appear in userinfo.

Permissions: instance administrator roles cover impersonation. IAM_ADMIN_IMPERSONATOR allows impersonating administrators and end users from all organizations, and IAM_END_USER_IMPERSONATOR allows impersonating end users. Give these roles to very few accounts, ideally in the dedicated administrator organization.

Use cases: a backend exchanging a user's token for one with another service's audience, or a support tool acting on behalf of a customer with the actor recorded in `act`.

## Checked
2026-11-08. Confirmed against the ZITADEL OIDC endpoints page (token exchange grant, supported client authentication options), the claims matrix (act claim in introspection, ID token and JWT access token, not userinfo) and the administrators guide (IAM_ADMIN_IMPERSONATOR and IAM_END_USER_IMPERSONATOR descriptions). Removed: the client_secret_post and client_secret_basic labels, which the page does not use for this grant.
Method: documentation only; no commands were run.
