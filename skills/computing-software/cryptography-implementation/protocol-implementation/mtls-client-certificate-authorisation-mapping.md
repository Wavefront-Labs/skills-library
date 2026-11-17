---
id: computing-software.cryptography-implementation.protocol-implementation.mtls-client-certificate-authorisation-mapping
name: mtls-client-certificate-authorisation-mapping
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, mutual-tls, mtls, client-certificate-auth, authorisation, x509]
level: practitioner
status: docs-checked
description: "Map an mTLS client certificate to an identity safely: Go ClientAuth policies, client CA pool, SAN identities, clientAuth EKU and what mTLS does not protect."
sources: ["https://www.rfc-editor.org/rfc/rfc8446#section-4.3.2", "https://www.rfc-editor.org/rfc/rfc5280#section-4.2.1.6", "https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html", "https://pkg.go.dev/crypto/tls#ClientAuthType"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client certificate authorisation mapping

TLS proves the client holds a key certified by a CA the server trusts. Which
identity that is, and what it may do, is application code.

## 1. Choose the verification policy (Go crypto/tls)

`tls.Config.ClientAuth` defaults to `NoClientCert`. The policies:

| Policy | Behaviour |
|---|---|
| `NoClientCert` | no certificate requested; any sent are not verified |
| `RequestClientCert` | requested, client need not send one |
| `RequireAnyClientCert` | at least one required, but not required to be valid |
| `VerifyClientCertIfGiven` | optional, but if sent it must be valid |
| `RequireAndVerifyClientCert` | at least one valid certificate required |

`ClientCAs` is the set of root CAs the server uses to verify client
certificates under that policy. With the optional policies, requests without
a certificate reach your handler, which must then reject them itself.
With `RequireAnyClientCert` the certificate is not validated, so never
treat it as authenticated.

## 2. Identity field

- RFC 5280 4.2.1.6: identities (email, DNS name, IP address, URI) are bound
  to the subject via the subject alternative name extension, which MUST be
  used when such identities are bound; the CA MUST verify all parts of it.
  Map identities from the SAN, not free-text subject fields.
- Several name forms may be present; decide which one your policy uses.

## 3. Purpose

- RFC 5280 defines `id-kp-clientAuth` (TLS WWW client authentication) as an
  extended key usage purpose. Applications MAY require the EKU extension and
  a particular purpose to accept a certificate; if both key usage and EKU are
  present, the certificate must only be used consistently with both.

## 4. What mTLS gives you (OWASP TLS cheat sheet)

- mTLS authenticates the client with a certificate and proof of its private
  key; in TLS 1.3 the proof is bound to the handshake transcript by
  CertificateVerify, so an intermediary cannot relay it to another connection.
- mTLS does not make data confidential from a TLS endpoint whose server
  certificate the client accepts; validate the server identity separately.
- Operational costs: issuing and managing client certificates is
  administratively heavy, and TLS decryption by organisations can break client
  certificate authentication.

## Verify

- [ ] A certificate from a CA outside `ClientCAs` is rejected at the handshake.
- [ ] A valid certificate with an unlisted identity gets 403.
- [ ] A certificate without the clientAuth purpose, or expired, fails.

## Checked

Method: docs-checked 2026-11-09 against pkg.go.dev/crypto/tls (ClientAuthType, Config.ClientAuth, ClientCAs), RFC 5280 (SAN section, EKU section), OWASP TLS Cheat Sheet (client certificates and mutual TLS). RFC 8446 section 4.3.2 listed but not needed for the retained claims. Removed: nginx directives, Java and OpenSSL purpose flags, claim that Go checks ExtKeyUsageClientAuth by default, CN deprecation, exact-match and issuer-keyed mapping advice, SPKI pinning, short-lived versus CRL advice, OPA and Envoy RBAC, proxy-termination section.
