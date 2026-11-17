---
id: computing-software.systems-network-administration.pki-tls-administration.mtls-identity-revocation
name: mtls-identity-revocation
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [mtls-identity-revocation, pki-mtls, mtls, client-identity, crl-checking, spiffe, pki-tls-administration]
level: practitioner
status: draft
description: "Map client certificate fields to identities, handle revocation for client certs and issue short-lived device certificates."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
  - https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# mTLS identity mapping and revocation
Goal: authorisation decisions based on certificate identity, with a removal path.
- Identity sources: SAN URI (SPIFFE ID), SAN email, DN CN/OU, or the issuing CA plus serial.
- Map in the proxy (`$ssl_client_s_dn`, Envoy `forward_client_cert_details`) and authorise in the app by ID, not by CN string match alone.
- Revocation options: CRL (`ssl_crl`, Envoy `crl`), OCSP, allow-list of serials, or short lifetimes (hours) with automated renewal.
- Prefer short-lived certs plus an authorisation list; large CRLs reload slowly and nginx needs reload to pick new files.
- Binding: tie issuance to device identity (TPM attestation, MDM enrolment) so stolen certs cannot be reissued.
- Log cert serial and subject on every request.
Gotcha: matching only `CN=` allows another CA's cert with the same CN if multiple client CAs are trusted; restrict trust to one CA per service.
Verify:
- [ ] Revoked or expired certs are rejected within the stated SLA.
- [ ] Logs show serial and subject for authenticated requests.
