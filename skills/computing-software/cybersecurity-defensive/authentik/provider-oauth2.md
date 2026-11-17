---
id: computing-software.cybersecurity-defensive.authentik.provider-oauth2
name: provider-oauth2
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, oauth2-provider, openid-connect, scopes, issuer-mode, redirect-uris, jwks]
level: advanced
status: docs-checked
description: "Reference for the authentik OAuth 2.0 / OIDC provider: endpoint paths, reserved slugs, redirect URIs, issuer mode, grant types, scopes, signing and JWE encryption."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/oauth2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: use authentik as an OpenID Provider (to use it as a Relying Party configure an OAuth/OIDC source instead).

## Endpoints
Authorization `/application/o/authorize/`, Token `/application/o/token/`, User Info `/application/o/userinfo/`, Revocation `/application/o/revoke/`, Introspection `/application/o/introspect/`, Device `/application/o/device/`; per application: `/application/o/<application_slug>/end-session/`, `.../jwks/`, `.../.well-known/openid-configuration`.
Application slugs `authorize`, `token`, `device`, `userinfo`, `introspect`, `revoke` are reserved.

Proxies, CDNs and WAFs must allow server-to-server calls to the OpenID configuration and JWKS endpoints; interactive challenges there cause validation failures and redirect loops. A 403 may be Cloudflare Browser Integrity Check rejecting non-standard user agents: add a narrow skip rule for that endpoint, not a global disable. JWKS is public by design.

Cross-provider introspection/revocation: add confidential provider B under **Federated OAuth2/OpenID Providers** of provider A, and authenticate with B's credentials (directional).

## Redirect URIs
If empty, authentik saves the URI used the first time a user opens the application. Regular expressions are allowed; escape literal periods as `\.`.

## Issuer mode
Default: per-provider issuer `https://authentik.company/application/o/<application_slug>/`. **Same identifier is used for all providers** gives `https://authentik.company/`; discovery stays under the per-application path.

## Grants and scopes
Authorization code (use PKCE for public clients), implicit (legacy, avoid), hybrid, client credentials, device code, token exchange, refresh token. Since 2024.2 a refresh token needs the client to request `offline_access` and the provider to include that scope mapping. Default scopes: `openid`, `profile`, `email`, `entitlements`, `offline_access`, `bound_key`; also `goauthentik.io/api`, `goauthentik.io/oidc/dcr` and GitHub-compatibility scopes. If no scope is requested, all configured scopes are treated as requested (not for token exchange). `email_verified` defaults to False since 2025.10.

Scope authorization via an expression policy on the application:
```python
if "my-admin-scope" in request.context["oauth_scopes"]:
    return ak_is_group_member(request.user, name="my-admin-group")
return True
```

## Signing and encryption
JWTs are always signed: with a **Signing Key** certificate asymmetrically (public key in JWKS), otherwise HS256 with the client secret (nothing in JWKS). Select an **Encryption Key** for JWE (RSA-OAEP-256 with A256CBC-HS512).

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/oauth2/.
Nothing was removed.
Method: documentation only; no commands were run.
