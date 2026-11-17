---
id: computing-software.cybersecurity-defensive.pomerium.jwt-sidecar-envoy
name: jwt-sidecar-envoy
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [envoy-sidecar, jwt-authn, remote-jwks, legacy-apps, sidecar]
level: advanced
status: docs-checked
description: "Protect an app that cannot validate JWTs by putting an Envoy jwt_authn sidecar in front that checks Pomerium's X-Pomerium-Jwt-Assertion header."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/getting-users-identity.mdx
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/mutual-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When app code cannot change, run a sidecar that checks Pomerium's token. Envoy's JWT Authn filter fetches the JWKS and rejects invalid tokens before requests reach the app.

Key configuration:
- Filter: `envoy.filters.http.jwt_authn`
- `providers` entry `pomerium` with `issuer` and `audiences` both set to the route host (e.g. `myapp.localhost.pomerium.io`)
- `from_headers`: `name: X-Pomerium-Jwt-Assertion`
- `remote_jwks.http_uri.uri`: `https://myapp.localhost.pomerium.io/.well-known/pomerium/jwks.json`, `cluster: egress-authenticate`, `timeout: 1s`
- `rules`: `match.prefix: /` with `requires.provider_name: pomerium`

Network layout from the mutual-auth guide: the service sits only on a `backend` network and only the sidecar container joins that network, so attackers cannot reach the service directly.
The app then needs no JWT logic. See verify-jwt-assertion for what the checks mean.

## Checked

2026-11-04. Confirmed against the Continuous Identity Verification and Mutual Authentication pages: filter name, provider settings, header, JWKS URI, cluster and timeout, rules, backend network layout. Removed an inferred sentence about bypass.

Method: documentation only; no commands were run.
