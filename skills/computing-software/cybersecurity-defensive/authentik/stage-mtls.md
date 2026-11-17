---
id: computing-software.cybersecurity-defensive.authentik.stage-mtls
name: stage-mtls
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, mutual-tls, client-certificates, mtls-stage, reverse-proxy, certificate-authorities]
level: advanced
status: docs-checked
description: "Set up the authentik Mutual TLS stage (Enterprise): mode, CAs, attribute matching and forwarding client certificates through nginx, ingress-nginx, Traefik or Envoy."
sources:
  - https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/mtls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: authenticate or enrol users by client certificate (local cert, smart card, PIV, hardware token). Enterprise feature.

## Options
**Mode** (optional or required), **Certificate authorities** (empty falls back to the active brand's client-certificate setting), **Certificate attribute** (subject, common name, email), **User attribute** (username, email). The stage does not authenticate on mere certificate presence; it compares the chosen certificate attribute with the chosen user attribute, so the mapping is as important as chain validation.

Do not use a publicly trusted CA for client authentication; use a private PKI trusted only by managed endpoints.

## Setup
1. Make the proxy (or brand) pass client certificates through.
2. **System > Certificates**: create or import the CA.
3. **Flows and Stages > Stages**: create a **Mutual TLS Stage**, set Mode, CAs and attribute mapping.
4. Bind it into the authentication or enrolment flow.

## Reverse proxy
The proxy must validate and forward the certificate.
- nginx:
```nginx
ssl_client_certificate /etc/ssl/path-to-my-ca.pem;
ssl_verify_client on;
proxy_set_header ssl-client-cert $ssl_client_escaped_cert;
```
- ingress-nginx annotations: `nginx.ingress.kubernetes.io/auth-tls-pass-certificate-to-upstream: "true"` and `nginx.ingress.kubernetes.io/auth-tls-secret: namespace/secretName` (the secret must contain `ca.crt`).
- Traefik: TLS option `clientAuth` with `caFiles` and `clientAuthType: RequireAndVerifyClientCert`, plus a `Middleware` with `passTLSClientCert: {pem: true}`.
- Envoy: see its mTLS and `x-forwarded-client-cert` docs.
- No reverse proxy: set trusted client CAs on the active brand.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/mtls/.
Removed as not confirmed by that page: post-success flow context claim.
Method: documentation only; no commands were run.
