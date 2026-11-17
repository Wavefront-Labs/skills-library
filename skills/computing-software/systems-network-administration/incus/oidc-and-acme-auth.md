---
id: computing-software.systems-network-administration.incus.oidc-and-acme-auth
name: oidc-and-acme-auth
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, authentication, oidc, openfga, device-authorization, acme, http-01, dns-01]
level: advanced
status: docs-checked
description: "Use OIDC login (device authorization grant, oidc.audience, allowed_subnets claim) with Incus, and ACME server certificates via the acme.* options."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/authentication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC and ACME

OIDC:
- Configure the `oidc.*` server options; the provider must support the Device Authorization Grant.
- `incus remote add <name> <address>`, then confirm the device code in a browser.
- Incus verifies JWT access tokens offline. Opaque tokens fall back to checking the ID token against the configured client ID, so do not share that client ID with other apps. Setting `oidc.audience` disables the fallback.
- Custom claim `incus.allowed_subnets` (list of CIDR strings) limits where a user may connect from.
- Every authenticated OIDC user gets full access, so pair OIDC with authorization (currently only OpenFGA).

ACME server certificate:
- Challenges: `HTTP-01` and `DNS-01`.
- Options: `acme.provider`, `acme.provider.environment`, `acme.eab.kid`, `acme.eab.hmac`.
- In a cluster the leader answers HTTP-01 and other members forward requests to it.

## Checked

2026-11-09. Confirmed against the Incus Remote API authentication page: Device Authorization Grant, offline JWT verification and opaque-token fallback, oidc.audience, incus.allowed_subnets claim, full access for OIDC users and OpenFGA as the only compatible authorization, HTTP-01 and DNS-01, acme.provider, acme.provider.environment, acme.eab.kid/hmac, cluster leader behaviour. Removed: the --auth-type=oidc flag (not on the page) and the vague other acme.* keys remark.
Method: documentation only; no commands were run.
