---
id: computing-software.systems-network-administration.pki-tls-administration.key-usage-eku
name: key-usage-eku
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [key-usage-eku, pki-x509-profile, pki, keyusage, extendedkeyusage, eku, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Choose keyUsage and extendedKeyUsage values for CA, TLS server, TLS client, code signing and S/MIME certificates."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key usage and extended key usage
Goal: certs that can do only the job they were issued for. Source: RFC 5280 sections 4.2.1.3 and 4.2.1.12.

## Rules from RFC 5280
- keyUsage MUST be included in certificates whose public keys validate signatures on other certificates or CRLs; when present, CAs SHOULD mark it critical.
- If the cA flag in basicConstraints is not asserted, the keyCertSign bit MUST NOT be asserted.
- extendedKeyUsage (EKU) is, in general, for end-entity certificates. It MAY be critical or non-critical, at the issuer's option.
- If EKU is present the certificate MUST only be used for one of the listed purposes. If both keyUsage and EKU are present, both are processed independently and the certificate may only be used for a purpose consistent with both; if none is, it MUST NOT be used.
- The RFC lists the key usage bits that may be consistent with each purpose:

| Purpose (EKU) | keyUsage bits that may be consistent |
|---|---|
| serverAuth (TLS server) | digitalSignature, keyEncipherment or keyAgreement |
| clientAuth (TLS client) | digitalSignature and/or keyAgreement |
| codeSigning | digitalSignature |
| emailProtection | digitalSignature, nonRepudiation, and/or (keyEncipherment or keyAgreement) |
| timeStamping | digitalSignature and/or nonRepudiation |
| OCSPSigning | digitalSignature and/or nonRepudiation |

- A CA signing certificates and CRLs uses keyCertSign and cRLSign.
- The special anyExtendedKeyUsage purpose lets a CA satisfy applications without restricting usage; CAs SHOULD NOT mark EKU critical if it is present.

## Example (OpenSSL config style, practitioner advice)
```
keyUsage = critical, digitalSignature
extendedKeyUsage = serverAuth, clientAuth
```
- Whether a given key needs keyEncipherment depends on key exchange; RFC 5280 lists the bits that may be consistent, it does not say which a given protocol version needs.
- Which EKUs a public TLS CA hierarchy may carry is set by browser root programs and the CA/Browser Forum, not by RFC 5280; confirm current rules with them.
- Some implementations treat an EKU on a CA certificate as a constraint on certificates it issues. RFC 5280 only says EKU is in general for end-entity certificates, so test your clients before adding EKU to an issuing CA.

## Verify
- [ ] Inspect the issued certificate's keyUsage and EKU (for example with `openssl x509 -noout -ext keyUsage,extendedKeyUsage`) and confirm they match the intended purpose.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read RFC 5280 sections 4.2.1.3 and 4.2.1.12 (criticality, bit/EKU consistency table, anyExtendedKeyUsage). The CA/Browser Forum documents index source was a landing page and was dropped. Removed as unsupported: the "TLS 1.3 and ECDHE do not need keyEncipherment" line, serverAuth-only roots and Chrome root program dates, the "EKU on an intermediate constrains all leaves" gotcha as a fact (kept as a hedged practitioner note), and the openssl verify -purpose check.
