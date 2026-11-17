---
id: computing-software.systems-network-administration.pki-tls-administration.ocsp-must-staple
name: ocsp-must-staple
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [ocsp-must-staple, pki-ocsp, ocsp, must-staple, tls-feature, rfc7633, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Issue and operate certificates with the TLS Feature must-staple extension, and understand the outage risk."
sources:
  - https://www.rfc-editor.org/rfc/rfc7633
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCSP Must-Staple
Goal: make clients refuse a certificate when the server does not return a stapled status response.
- Extension: TLS feature (`id-pe-tlsfeature`, `{ id-pe 24 }`, that is 1.3.6.1.5.5.7.1.24 under the PKIX extensions arc). Its value is a SEQUENCE of TLS extension identifiers; listing `status_request` makes it "must-staple".
- It SHOULD NOT be marked critical (RFC 7633 section 4): a critical flag makes clients that do not understand it reject the certificate.
- A server MAY ask for it by putting the extension in the CSR as a CSR attribute. A CA SHOULD NOT issue it without an affirmative statement that the subscriber intends to support the feature.
- A server whose certificate carries it MUST support the feature (return a stapled response).
- Clients: a client MUST treat the certificate as invalid if the server does not offer the features in both the ClientHello and the extension. If TLS with a valid certificate is mandated, it MUST refuse; otherwise it MAY accept the connection but MUST NOT treat the certificate as valid. It MAY accept if validity is established another way (for example OCSP data from another source).
- Outage risk: a server that lacks a fresh response cannot comply, so a stapling failure becomes a client-visible failure. Monitor stapling and the age of the staple.
- Issuance order (section 4.3): the CA SHOULD publish the OCSP token before releasing the certificate; when replacing a certificate the server SHOULD NOT start using the new one until the needed status token is available.
- A server SHOULD verify its configuration is compatible with the extension and tell the administrator about inconsistencies.
- A CA certificate with the extension constrains chains: certificates it signs MUST carry the same or a superset of the features.
- Which browsers enforce it, and which public CAs still issue it, are not covered by RFC 7633: check the browser and CA policies in force.
Verify:
- [ ] The certificate text shows a TLS Feature extension naming `status_request`, not marked critical.
- [ ] The server returns a staple before a new certificate goes live, and an alert exists on the staple's `Next Update` age.

## Checked
Confirmed 2026-11-08 against RFC 7633 (sections 3, 4, 4.1 to 4.3, 5). Removed: openssl req and certbot commands (not in the RFC), "Firefox enforces, Chrome does not", the Let's Encrypt statement, and the nginx/Apache restart gotcha (all outside the cited page).
Method: docs-only read of cited pages, 2026-11-08
