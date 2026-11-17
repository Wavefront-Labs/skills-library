---
id: computing-software.cybersecurity-defensive.pomerium.jwt-bearer-token-routes
name: jwt-bearer-token-routes
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [jwt-bearer, identity-providers, jwks-url, machine-to-machine, spiffe]
level: advanced
status: docs-checked
description: "Accept bearer JWTs from trusted issuers on a Pomerium route using bearer_token_format jwt and identity_providers, including SPIFFE and GitHub Actions."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/bearer-token-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Services and CI jobs can call upstreams with `Authorization` bearer tokens, with no browser redirect.

`bearer_token_format` values: `default`, `idp_access_token`, `idp_identity_token` (tokens from the sign-in IdP) and `jwt` (verifiable JWTs from any trusted issuer).

With `jwt`, Pomerium fetches and caches the issuer's JWKS once (no per-request IdP call), verifies signature, `iss`, `exp`, `nbf` and `aud`, then evaluates route policy on the claims.

`identity_providers` is a map keyed by a name you choose. These providers only verify JWT bearer tokens and do not replace the interactive `idp_*` provider. Per provider: `issuer`, `jwks_url`, `supported_algs`, `audiences`.

On the route set `bearer_token_format: jwt`, optionally an `identity_providers` allowlist (if unset all providers are used), and a policy using `claim/<name>`; dots descend into nested claims.

Other issuers that publish a JWKS work too:
- SPIFFE JWT-SVIDs: trust the authority's issuer (typically `ES256`) and authorize on `claim/sub`.
- GitHub Actions OIDC: trust `https://token.actions.githubusercontent.com`; authorize on `claim/repository` or `claim/ref`; set `audiences` to what the workflow requests.

## Checked

2026-11-04. Confirmed against the Bearer Token Access page: bearer_token_format values, JWKS fetched once and cached, verified claims, identity_providers map and per-provider keys, route allowlist, claim/ criterion, SPIFFE and GitHub Actions notes. Nothing removed.

Method: documentation only; no commands were run.
