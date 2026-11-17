---
id: computing-software.systems-network-administration.pki-tls-administration.x509-base-fields
name: x509-base-fields
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [x509-base-fields, pki-x509-profile, pki, x509, rfc5280, tbscertificate, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Read and set TBSCertificate fields: version, serial, validity, signature algorithm, issuer, subject, SPKI and encoding rules for each."
sources:
  - https://www.rfc-editor.org/rfc/rfc5280
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X.509 base fields and encoding
Goal: know the TBSCertificate fields and what the RFC 5280 profile requires of each (section 4.1).

- version: when extensions are used, as expected in this profile, version MUST be 3 (encoded value 2).
- serialNumber: a positive integer assigned by the CA, unique for each certificate issued by that CA (issuer name plus serial identify one certificate). Conforming CAs MUST NOT use serial numbers longer than 20 octets, and certificate users MUST handle values up to 20 octets.
- signature: the algorithm identifier in the TBSCertificate MUST contain the same algorithm identifier as the outer signatureAlgorithm field. A mismatch makes the certificate invalid under the profile.
- validity (notBefore, notAfter): each may be UTCTime or GeneralizedTime. The profile requires UTCTime for dates through the year 2049 and GeneralizedTime for 2050 and later.
- subject: where non-empty it MUST be an X.500 distinguished name that is unique per subject entity certified by one CA; the subject can be empty when a critical subjectAltName carries the identity.
- issuerUniqueID and subjectUniqueID: conforming CAs MUST NOT generate certificates with unique identifiers.

## Practitioner advice (not from RFC 5280)
- Use random serial numbers with plenty of entropy and keep them under the 20-octet limit; check the CA/Browser Forum rules if you issue public TLS certificates.
- Backdate notBefore a few minutes if clocks may be skewed.
- Choose signature and key algorithms to suit your clients; confirm client support for newer algorithms before issuing.
- To inspect a certificate, `openssl x509 -in cert.pem -noout -text` and `openssl asn1parse -in cert.pem` show the fields.
- Run a certificate linter (zlint or pkilint) against your profile in CI.

## Verify
- [ ] Version is 3, the serial is positive and at most 20 octets, the dates look sane and the inner and outer signature algorithms match.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read RFC 5280 section 4.1 (version, serialNumber, signature, validity, unique identifiers). Removed as unsupported: the 64-bit public CA entropy figure, the specific algorithm names, the RSA 2048/3072 and P-256/P-384 sizes, and the no_sigdump openssl option. Practitioner advice is marked.
