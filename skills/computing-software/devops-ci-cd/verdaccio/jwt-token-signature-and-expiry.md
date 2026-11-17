---
id: computing-software.devops-ci-cd.verdaccio.jwt-token-signature-and-expiry
name: jwt-token-signature-and-expiry
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [jwt, token-expiry, security-api, jwt-signature, expiresin, token-lifetime]
level: practitioner
status: docs-checked
description: "Switch the Verdaccio API from non-expiring legacy tokens to JWT with sign.expiresIn, and tune the separate web token lifetime under security.web."
sources:
  - https://verdaccio.org/docs/configuration/
  - https://verdaccio.org/docs/best/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Legacy tokens (AES, aes-256-ctr) never expire. Add a `jwt` block under `security.api` to get expiring JWTs; without it the legacy signature is used. The web UI always uses JWT (1 hour by default).

```yaml
security:
  api:
    jwt:
      sign:
        expiresIn: 29d
        notBefore: 0
      verify:
        someProp: [value]
  web:
    sign:
      expiresIn: 1h
    verify:
      someProp: [value]
```
Benefit from the best practices page: with JWT the registry relies on the token signature, avoiding an auth-plugin call per request (the legacy system unpacks and validates credentials every time).

Gotchas:
- `security.api.legacy: true` is the default even when the section is absent.
- npmjs and legacy Verdaccio tokens never expire unless invalidated manually.
- The secret signs tokens; replacing it invalidates them (see storage-and-secret).

## Checked

2026-11-04. Read the Verdaccio documentation pages: Configuration (Security, JWT Token Signature) and Best Practices (Expiring Tokens). Confirmed: legacy tokens never expiring, the jwt block under security.api, the web 1 hour default, notBefore, the JWT performance benefit, legacy as default and the secret invalidating tokens. Removed or corrected: the unconfirmed verify line about the new token being a JWT.

Method: documentation only; no commands were run.
