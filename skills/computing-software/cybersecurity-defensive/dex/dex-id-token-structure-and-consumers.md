---
id: computing-software.cybersecurity-defensive.dex.dex-id-token-structure-and-consumers
name: dex-id-token-structure-and-consumers
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [id-token, jwt, claims, oidc]
level: intro
status: docs-checked
description: "Understand the ID token Dex signs: standard claims, groups and email claims, and why Kubernetes and AWS STS can consume it directly."
sources:
  - https://dexidp.io/docs/configuration/tokens/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ID tokens are Dex's primary output. They are JSON Web Tokens signed by Dex and returned in the OAuth2 response to attest to the end user's identity.

A typical decoded payload contains:

```json
{
  "iss": "http://127.0.0.1:5556/dex",
  "sub": "CgcyMzQyNzQ5EgZnaXRodWI",
  "aud": "example-app",
  "exp": 1492882042,
  "iat": 1492795642,
  "at_hash": "bi96gOXZShvlWYtal9Eqiw",
  "email": "jane.doe@coreos.com",
  "email_verified": true,
  "groups": ["admins", "developers"],
  "name": "Jane Doe"
}
```

The claims say which client app logged the user in (`aud`), when the token expires (`exp`) and who the user is.

Because the tokens are signed and use standard claims, other services can accept them as service-to-service credentials. The docs name Kubernetes and AWS STS as systems that already consume Dex-issued ID tokens.


## Checked

2026-11-08: Read the Dex Tokens page in full. Confirmed the ID token description, the example payload, the standard claims purpose and the Kubernetes and AWS STS consumers. Removed the scope dependence claim, the issuer check and the signing key verification note, which that page does not state.
Method: documentation only; no commands were run.
