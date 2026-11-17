---
id: computing-software.web-development.hasura.hasura-jwt-authentication
name: hasura-jwt-authentication
category: computing-software
field: web-development
product: hasura
tags: [hasura, authentication, jwt, claims-map, jwk, admin-secret]
level: advanced
status: docs-checked
description: "Configure Hasura JWT mode with HASURA_GRAPHQL_JWT_SECRET, including type and key or jwk_url, claims namespace and claims_map."
sources:
  - https://github.com/hasura/graphql-engine/blob/master/docs/docs/auth/authentication/jwt.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate clients with JWTs from your identity provider.

Prerequisite: secure the GraphQL endpoint first (admin secret); JWT mode only takes effect on a secured endpoint. Then set the env var `HASURA_GRAPHQL_JWT_SECRET` (flag `--jwt-secret`) to a JSON object:

```json
{ "type": "RS256", "jwk_url": "https://<IDP_HOST>/.well-known/jwks.json" }
```
or, with a shared key:

```json
{ "type": "HS256", "key": "<AT_LEAST_32_CHARACTERS_SECRET>" }
```
Config keys per the docs: `type`, `key`, `jwk_url`, `claims_namespace`, `claims_namespace_path`, `claims_format` (`json` or `stringified_json`), `audience`, `issuer`, `claims_map`, `allowed_skew` (seconds of clock-skew leeway), `header` and `extra_required_claims` (any of `"audience"`, `"issuer"`). As a minimum, either `type` and `key`, or `jwk_url`, must be present. Algorithms: HS256/384/512, RS256/384/512, Ed25519, ES256/384/512. For asymmetric algorithms `key` is the public key only (PEM string or X509 certificate).

Clients send `Authorization: Bearer <JWT>`.

By default the token must contain, under the namespace `https://hasura.io/jwt/claims` (changeable with `claims_namespace` or `claims_namespace_path`), the claims `x-hasura-default-role` and `x-hasura-allowed-roles`. Other `x-hasura-*` claims are optional and their values are strings. The client may send an `x-hasura-role` header to pick one of the allowed roles; otherwise the default role is used.

To read claims from other places use `claims_map`:

```json
"claims_map": {
  "x-hasura-allowed-roles": { "path": "$.roles" },
  "x-hasura-default-role": "user",
  "x-hasura-user-id": { "path": "$.user.id" }
}
```
A path can also carry a fallback: `{ "path": "$.roles.default", "default": "user" }`. If `claims_map` is set, `claims_namespace`, `claims_namespace_path` and `claims_format` are ignored.

Gotchas:
- HS256 keys must be at least 32 characters.
- Set `audience` (and `issuer`) so tokens meant for other tenants are rejected; the docs call omitting `audience` where the provider issues shared tokens a major security risk. Tokens that omit `aud` or `iss` are still accepted unless you add them to `extra_required_claims`.
- A `jwk_url` is refreshed automatically only when the provider sends `Cache-Control` (`max-age`, `s-maxage`, `no-cache`, `no-store`, `must-revalidate`) or `Expires` headers.

## Checked

2026-11-04. Confirmed against the cited pages: jwt page: prerequisite, config object, minimum keys, algorithms, key rules, default namespace and mandatory claims, role header, claims_map forms and precedence, audience/issuer/extra_required_claims behaviour, 32-char HS256 rule, JWK refresh rules. Removed or corrected: the wrong 'admin secret' prerequisite wording (the page says secure the endpoint), the claims_map precedence wording and the Verify step.

Method: documentation only; no commands were run.
