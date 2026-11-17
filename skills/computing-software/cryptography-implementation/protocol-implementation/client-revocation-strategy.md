---
id: computing-software.cryptography-implementation.protocol-implementation.client-revocation-strategy
name: client-revocation-strategy
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, ocsp-must-staple, revocation, ocsp, crl, crlite, crlsets, short-lived-certificates, certificate-validation, private-pki]
level: advanced
status: docs-checked
description: "Decide how clients handle revocation: why Let's Encrypt moved from OCSP to CRLs, OCSP must-staple semantics, and what breaks in non-browser clients."
sources: ["https://letsencrypt.org/2024/12/05/ending-ocsp/", "https://www.rfc-editor.org/rfc/rfc7633"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client revocation strategy

## What the sources establish
| Mechanism | Confirmed facts |
|---|---|
| Online OCSP | When a client checks via OCSP, the CA's responder learns which site is visited from that client's IP address; Let's Encrypt cites this privacy risk as its main reason for ending OCSP. CRLs do not have the issue. |
| OCSP stapling | The web server sends a copy of the OCSP response in the TLS handshake so the client need not contact the CA. |
| OCSP Must Staple (RFC 7633 TLS Feature extension) | A client that sees the extension in a certificate must expect a stapled response; if it cannot get a valid one it must refuse the connection (RFC 7633 section 4.2.3.1 and the client rules). Let's Encrypt says it never gained wide browser support and popular web servers implement stapling in ways that risk downtime. |
| CRLs | Let's Encrypt added CRL support in 2022 and says CRLs have wide browser support and privacy benefits without special web server configuration. |

## Let's Encrypt timeline (announced Dec 2024)
- 30 Jan 2025: Must-Staple issuance requests fail unless the account previously issued such a certificate.
- 7 May 2025: CRL URLs added to certificates and OCSP URLs dropped; all Must-Staple requests fail, including renewals.
- 6 Aug 2025: OCSP responders turned off.

## For non-browser software
- Let's Encrypt warns that non-browser software (its example is a VPN) must keep working when a certificate has no OCSP URL.
- Remove any ACME client configuration that requests the Must Staple extension.

## Verify
- [ ] Clients and servers still validate correctly against certificates with no OCSP URL.
- [ ] No issuance configuration requests Must Staple.

## Checked
Method: docs-checked 2026-11-09 against the Let's Encrypt "Ending OCSP Support in 2025" post (full) and RFC 7633 text (extension semantics and client rules).
Removed as unconfirmed by the cited pages: CRLSets and CRLite descriptions, "OCSP optional for public CAs" and "CRLs mandatory again" (the CA/B Forum cited page is only a document index), 6-day certificate availability, the private PKI option table, and the advice on stale-CRL grace periods. The CA/B Forum source was dropped as unread.
