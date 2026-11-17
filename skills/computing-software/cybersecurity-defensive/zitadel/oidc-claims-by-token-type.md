---
id: computing-software.cybersecurity-defensive.zitadel.oidc-claims-by-token-type
name: oidc-claims-by-token-type
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, oidc, claims, id-token, userinfo, introspection]
level: advanced
status: docs-checked
description: "Check where ZITADEL asserts each claim across userinfo, introspection, ID token and access token, and why profile claims are missing from tokens."
sources:
  - https://zitadel.com/docs/apis/openidoauth/claims
  - https://zitadel.com/docs/apis/openidoauth/endpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL publishes a matrix of where each claim appears: userinfo, introspection, ID token and access token.

Examples from the matrix:

- `acr`, `amr` and `auth_time` appear only in the ID token.
- `aud`, `azp`, `exp` and `iat` appear in introspection and the ID token, and in the access token when it is a JWT. For introspection `azp` is returned as the client id.
- `email`, `email_verified`, `family_name`, `given_name`, `gender` and `address` appear in userinfo and introspection when requested. In the ID token they appear when requested and the response type is `id_token`. They never appear in the access token.
- `act` appears only after a token exchange with an `actor_token`.

Per the OIDC Core specification, when an access token is issued the ID token does not contain claims of the `profile`, `email`, `phone` and `address` scopes. Fetch them from the userinfo or introspection endpoint, or turn on the application option `id_token_userinfo_assertion`, labelled "User Info inside ID Token" in the console.

When a claim is missing, check the table first, then the scopes you requested, then that option.

## Checked

2026-11-08. Read in full: the claims page. Partial read: the endpoints page (about 29k characters) was searched only for the id_token and userinfo assertion text, which confirms the OIDC Core note and the id_token_userinfo_assertion option.

Method: documentation only; no commands were run.
