---
id: computing-software.cybersecurity-defensive.pomerium.direct-idp-token-auth
name: direct-idp-token-auth
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [idp-access-token, bearer-token-format, cli-automation, authorization-header, token-validation]
level: practitioner
status: docs-checked
description: "Let CLI tools and automation present an IdP access or identity token directly to Pomerium instead of a browser login, and what Pomerium validates."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/authentication.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Users can skip the browser redirect by presenting an IdP access or identity token directly.

How it is sent:
- An `Authorization: Bearer <token>` header, or the Pomerium CLI.

What Pomerium does:
- Validates the token's signature and claims with the IdP (for example expiry and client).
- Trusts only configured IdPs.

It is opt-in and is enabled through the bearer token format setting (see the Bearer Token Format reference). Typical uses are CLI tools and automation; the page cites `az login` as an example.

For machine tokens from other issuers (for example Kubernetes service accounts), use the `jwt` bearer token format instead; see jwt-bearer-token-routes.

## Checked

2026-11-04. Confirmed against the Authentication page: direct IdP token authentication, Authorization Bearer or Pomerium CLI, az login example, signature and claim validation, trusted IdPs only, opt-in via bearer token format. Nothing removed.

Method: documentation only; no commands were run.
