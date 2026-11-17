---
id: computing-software.cybersecurity-defensive.pomerium.verify-jwt-assertion
name: verify-jwt-assertion
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [jwt-assertion, jwks, x-pomerium-jwt-assertion, continuous-verification, kid-claim]
level: practitioner
status: docs-checked
description: "Verify the Pomerium X-Pomerium-Jwt-Assertion token in an upstream app: signature via JWKS, audience, issuer and expiry, plus manual testing."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/getting-users-identity.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium signs a JWT per verified request and sends it in the `X-Pomerium-Jwt-Assertion` header. The original IdP ID token is never forwarded.

Claims: `exp`, `iat`, `sub`, `aud`, `iss`, plus `email`, `groups` (if available) and `name` (if provided).

Verify:
1. Signature, with Pomerium's key.
2. `aud` and `iss` match the service domain.
3. `exp` is later than now.

Fetch keys:

```
curl https://<YOUR-SERVICE-DOMAIN>/.well-known/pomerium/jwks.json -H 'Accept: application/json'
```

Pick the key whose ID matches the `kid` in the JWT header. Trust `email` and `groups` only after validation.

Options: apps with built-in JWT support (e.g. Grafana: point it at the JWKS endpoint), custom code with a JWT library or Pomerium SDK (Go, Node/JS), or an Envoy sidecar (see jwt-sidecar-envoy). If `issuer` and `audience` are unset in the JS SDK it uses trust-on-first-use; set them explicitly in production.

Manual check: generate a key with `openssl ecparam -genkey -name prime256v1 -noout -out ec_private.pem`, derive the public key with `openssl ec`, give Pomerium the base64 private key as `SIGNING_KEY`, decode the header token (e.g. jwt.io) and paste the public key to confirm.

## Checked

2026-11-04. Confirmed against the Continuous Identity Verification page: header name, claims list, three checks, JWKS URL and curl, kid selection, openssl ecparam steps, SIGNING_KEY, Grafana, JS SDK trust-on-first-use. Nothing removed.

Method: documentation only; no commands were run.
