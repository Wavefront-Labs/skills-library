---
id: computing-software.cybersecurity-defensive.pomerium.service-account-auth-headers
name: service-account-auth-headers
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [authorization-header, x-pomerium-authorization, service-account-jwt, curl, header-schemes]
level: intro
status: docs-checked
description: "Send a Pomerium service account JWT using any of the three accepted header formats, with a curl example."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/service-accounts.md
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/programmatic-access.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium accepts its JWT (a service account token or a programmatic login token) in three forms:

- `Authorization: Bearer Pomerium-${pomerium_jwt}`
- `X-Pomerium-Authorization: ${pomerium_jwt}`
- `Authorization: Pomerium ${pomerium_jwt}`

Example (bearer form):

```
curl -i -H "Accept: application/json" -H "Authorization: Bearer Pomerium-${pomerium_jwt}" https://verify.localhost.pomerium.io
```

A valid request returns `HTTP/2 200`.

The route's policy must allow the account, for example through a `User` criterion matching the service account's User ID (see create-service-account).

For tokens from external issuers such as Kubernetes or GitHub Actions use plain `Authorization: Bearer` with the `jwt` bearer token format instead (see jwt-bearer-token-routes).

## Checked

2026-11-04. Confirmed against the Service Accounts and Programmatic access pages: the three header forms, the curl example, HTTP/2 200 result, User criterion matching the User ID, and the jwt bearer format for external issuers (Bearer Token Access page). Nothing removed.

Method: documentation only; no commands were run.
