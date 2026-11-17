---
id: computing-software.cybersecurity-defensive.pomerium.mutual-auth-methods
name: mutual-auth-methods
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [mutual-authentication, mtls, pass-identity-headers, east-west, perimeter-bypass]
level: practitioner
status: docs-checked
description: "Choose between basic, JWT-verification, mTLS and sidecar mutual authentication between Pomerium and upstream services."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/mutual-auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Mutual authentication means both parties verify each other before communicating.

1. **Basic**: user is redirected to the IdP and Pomerium authorizes before contacting the upstream. Security moderate, no mutual auth. Weakness: it relies on the network perimeter, so an attacker who bypasses the firewall can reach the upstream directly.
2. **JWT verification** (application layer; security strong, difficulty moderate): `pass_identity_headers` forwards the signed JWT in `X-Pomerium-JWT-Assertion`; the upstream verifies it against Pomerium's JWKS. A forged JWT is rejected because the attacker cannot sign with Pomerium's key.
3. **mTLS** (protocol layer; difficulty hard): after HTTPS the server requests a client certificate and validates its signing authority. East-west mTLS between Pomerium and each upstream is configured once per service; per-end-user mTLS is cumbersome.
4. **Sidecar**: software that does JWT or mTLS checks for a service not built for it. The service is reachable only on a private `backend` network shared with the sidecar.
5. **Combined**: users go through IdP login, Pomerium uses mTLS with the app and passes the JWT; admin routes additionally require a client certificate; an API accepts only mTLS from the proxy.

See verify-jwt-assertion, downstream-mtls-mkcert and upstream-mtls-openssl.

## Checked

2026-11-04. Confirmed against the Mutual Authentication page: the five scenarios, their security and difficulty labels, pass_identity_headers, X-Pomerium-JWT-Assertion, east-west mTLS once per service, sidecar backend network, combined example. Nothing removed.

Method: documentation only; no commands were run.
