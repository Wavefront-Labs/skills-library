---
id: computing-software.cybersecurity-defensive.zitadel.oidc-endpoints-and-discovery
name: oidc-endpoints-and-discovery
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, oidc, endpoints, discovery, authorize, token]
level: practitioner
status: docs-checked
description: "Locate ZITADEL's OIDC discovery document and core endpoints, and send a valid authorization request."
sources:
  - https://zitadel.com/docs/apis/openidoauth/endpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Everything starts from the discovery document at `${CUSTOM_DOMAIN}/.well-known/openid-configuration`, located within the issuer domain.

Core endpoints:

- Authorization: `${CUSTOM_DOMAIN}/oauth/v2/authorize`. It lives with the login page, because it needs the same cookie domain. It begins every initial user authentication.
- Token, introspection (`/oauth/v2/introspect`), userinfo, revocation (`/oauth/v2/revoke`), end session (`/oidc/v1/end_session`) and JWKS (`/oauth/v2/keys`).
- A registration endpoint (OAuth 2.0 Dynamic Client Registration) is documented. It is disabled by default and is advertised in the discovery document only when enabled in the instance security settings. ZITADEL does not provide an OAuth 2.0 metadata endpoint; use the OIDC discovery document instead.

Required authorization request parameters:

- `client_id`: the id shown in the console
- `redirect_uri`: must match exactly one URI preregistered in the console
- `response_type`: `code` for most use cases; `id_token token` or `id_token` are the alternatives
- `scope`: space delimited, and `openid` is required

Token endpoint client authentication depends on the application: a client secret in a Basic header, `client_id` and `client_secret` in the body, PKCE (the client sends `client_id` and `code_verifier`, with `code_challenge_method` S256), or a `client_assertion` JWT (private key JWT).

Read the discovery document rather than hard-coding endpoint paths, and use the issuer of your custom domain so tokens validate against the right instance.

## Checked
2026-11-08. Confirmed against the ZITADEL OIDC endpoints page: discovery path, authorize endpoint and cookie-domain note, required request parameters, endpoint paths, and client authentication options. Added: registration endpoint is disabled by default and there is no OAuth 2.0 metadata endpoint. Removed: the client_secret_post label, which the page does not use.
Method: documentation only; no commands were run.
