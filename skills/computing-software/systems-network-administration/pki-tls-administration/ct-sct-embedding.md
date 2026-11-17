---
id: computing-software.systems-network-administration.pki-tls-administration.ct-sct-embedding
name: ct-sct-embedding
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [ct-sct-embedding, pki-ct, certificate-transparency, sct, rfc6962, precertificate, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Understand CT precertificates, SCT embedding, TLS extension and OCSP delivery, and the SCT counts Chrome requires."
sources:
  - https://www.rfc-editor.org/rfc/rfc6962
  - https://googlechrome.github.io/CertificateTransparency/ct_policy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CT logs and SCT delivery
Goal: know how a publicly trusted cert proves it was logged.
- A CA may submit a Precertificate to logs before issuance. It is the certificate to be issued plus a critical poison extension (OID 1.3.6.1.4.1.11129.2.4.3, value ASN.1 NULL) so a standard X.509 client cannot validate it. The log returns an SCT.
- The CA can embed the SCTs from one or more logs in the final certificate as an X.509v3 extension (OID 1.3.6.1.4.1.11129.2.4.2); clients reconstruct the original TBSCertificate to verify the SCT signature.
- RFC 6962 delivery options in the TLS handshake: the certificate extension, a TLS extension of type `signed_certificate_timestamp`, or OCSP stapling with an OCSP extension (OID 1.3.6.1.4.1.11129.2.4.5). At least one SCT must be included.
- Chrome policy (page read, current text): an "embedded SCT" is one in the SignedCertificateTimestampList extension of the certificate. Most TLS servers do not support the TLS extension, so CAs should embed SCTs to validate in Chrome.
- Chrome counts for embedded SCTs: certificate lifetime up to 180 days needs SCTs from 2 distinct logs, over 180 days needs 3, with at least two from distinct log operators, and at least one from a log that is Qualified, Usable or ReadOnly at check time.
- Chrome counts for SCTs delivered via TLS: at least two SCTs from logs that were Qualified, Usable or ReadOnly at check time, from distinct log operators.
- Chrome accepts SCTs in stapled OCSP responses only in versions before 148.
- A certificate that is not CT compliant is not mis-issuance under Chrome's root program; it fails to validate in CT-enforcing Chrome.
- Chrome enforces CT only while its freshest log list is within the past 70 days.
Gotcha: CT logs make issued certificates publicly visible, so hostnames in publicly trusted certificates are public.
Verify:
- [ ] The certificate carries the required number of SCTs for its lifetime.

## Checked
Method: docs-checked 2026-11-09 against RFC 6962 (precertificates, poison extension, SCT delivery section 3.3) and the Chrome Certificate Transparency Policy page (read in full). Removed: the `openssl` grep command, the crt.sh link, log sharding by expiry year, "private CAs may skip CT" and the wildcard advice for internal names (none stated on the pages read), and the Apple policy claim in the description.
