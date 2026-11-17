---
id: computing-software.systems-network-administration.pki-tls-administration.acme-order-flow
name: acme-order-flow
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [acme-order-flow, pki-acme-protocol, acme, rfc8555, jws, order, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Walk the ACME flow: directory, newAccount, newOrder, authorizations, finalize with CSR and certificate download, with JWS and nonce rules."
sources:
  - https://www.rfc-editor.org/rfc/rfc8555
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACME account, order and finalise flow
Goal: understand each request when debugging a client or server.
1. GET `directory` returns URLs for newNonce, newAccount, newOrder, revokeCert, keyChange.
2. HEAD newNonce gives a `Replay-Nonce`; every POST carries a fresh nonce in the JWS protected header with `url` and `kid` (or `jwk` for newAccount).
3. POST newAccount (contact, termsOfServiceAgreed) returns an account URL (the `kid`).
4. POST newOrder with `identifiers` (type dns, value) returns authorization URLs.
5. For each authz pick a challenge, publish the proof, POST `{}` to the challenge URL, poll authz until `valid`.
6. POST finalize with base64url DER CSR; poll the order until `valid`.
7. POST-as-GET the `certificate` URL to download the PEM chain.
Statuses: pending, ready, processing, valid, invalid.
Gotcha: `badNonce` errors are normal; clients must retry once with the nonce from the error response.
Verify:
- [ ] `curl -s https://acme-v02.api.letsencrypt.org/directory` lists the endpoints.
- [ ] Your client's debug or verbose log shows the sequence above completing with a certificate.

## Checked
2026-11-03. Confirmed in RFC 8555: the directory resource, newNonce and the `Replay-Nonce` header, newAccount with `termsOfServiceAgreed`, newOrder identifiers, authorizations and challenges, finalize with a base64url DER CSR, POST-as-GET, order and authorization statuses, and `badNonce` retry; the Let's Encrypt directory URL was fetched. Removed: the client-specific `--debug` flag.
Method: documentation only; no commands were run.
