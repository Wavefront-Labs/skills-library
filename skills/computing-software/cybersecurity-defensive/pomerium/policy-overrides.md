---
id: computing-software.cybersecurity-defensive.pomerium.policy-overrides
name: policy-overrides
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [public-access, cors-preflight, any-authenticated-user, policy-override, robots-txt]
level: practitioner
status: docs-checked
description: "Use Pomerium policy overrides (any authenticated user, CORS preflight, public access) safely, including the robots.txt behaviour on public routes."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/authorization.mdx
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/ppl.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Policy overrides apply to both PPL and Rego and bypass the other policy logic.

- **Any Authenticated User**: admits any logged-in user. In PPL this matches the `authenticated_user` criterion and the `allow_any_authenticated_user` option.
- **CORS Preflight**: `OPTIONS` requests pass without authentication. The PPL `cors_preflight` criterion is true for `OPTIONS` requests that include both `Access-Control-Request-Method` and `Origin` headers.
- **Public Access**: no authentication required. The docs say to use it with caution. It matches the PPL `accept` criterion and `allow_public_unauthenticated_access`.

Caveat: on a fully public route, `robots.txt` is proxied from the upstream service instead of Pomerium returning a default disallow response.

## Checked

2026-11-04. Confirmed against the Authorization and PPL pages: the three overrides, robots.txt note, and the authenticated_user, cors_preflight and accept criteria with their equivalent options. Removed a closing recommendation the pages do not state.

Method: documentation only; no commands were run.
