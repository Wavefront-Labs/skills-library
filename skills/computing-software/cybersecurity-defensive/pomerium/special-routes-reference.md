---
id: computing-software.cybersecurity-defensive.pomerium.special-routes-reference
name: special-routes-reference
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [pomerium-endpoints, well-known-pomerium, jwks-json, hpke-public-key, healthz]
level: intro
status: docs-checked
description: "Reference the reserved /.pomerium and /.well-known/pomerium endpoints that the proxy handles itself and never forwards upstream."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/special-routes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Reserved `/.pomerium` routes are handled by the proxy and never forwarded upstream.

Require login:
- `/.pomerium/`: HTML page with identity, session and device IDs; devices can be removed.
- `/.pomerium/user`: claims as JSON. For UI customisation only; backends must enforce permissions themselves.
- `/.pomerium/webauthn`: WebAuthn enrollment (GET challenge, POST attestation; CSRF token needed).
- `/.pomerium/device-enrolled`: post-enrollment confirmation.

Other:
- `/.pomerium/api/v1/login`: no session needed; returns a one-time programmatic login URL (see programmatic-login).
- `/.pomerium/sign_out`: GET or POST with CSRF token; clears the session and follows `pomerium_redirect_uri`.

Unauthenticated control plane endpoints:
- `/ping` and `/healthz`: 200 OK for load balancers and probes.
- `/.well-known/pomerium`: discovery document with `issuer`, `authentication_callback_endpoint`, `frontchannel_logout_uri`, `jwks_uri`.
- `/.well-known/pomerium/jwks.json`: public keys for Pomerium-issued JWTs. Keys rotate; respect `Cache-Control` and `ETag`.
- `/.well-known/pomerium/hpke-public-key`: used by the stateless authentication flow.

Some endpoints may be deprecated or off by default in newer versions, and some behave differently in stateless mode; check upgrade notes.

## Checked

2026-11-04. Read the Special Routes page: the route table, authentication requirements, user endpoint warning, webauthn and sign_out behaviour, health endpoints, discovery document keys, JWKS caching advice, HPKE purpose and the deprecation note confirmed. Nothing removed.

Method: documentation only; no commands were run.
