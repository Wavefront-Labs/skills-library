---
id: computing-software.cryptography-implementation.openssl.aia-and-crl-distribution-point-extensions
name: aia-and-crl-distribution-point-extensions
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, crl-distribution-points, authority-information-access, aia, ocsp, x509v3-extensions, openssl-ca]
level: practitioner
status: verified
description: "Configure AIA (caIssuers, OCSP) and CRL distribution point extensions in OpenSSL CA configs: HTTP URLs, per-CA sections, and testing that clients can fetch them."
sources: ["https://docs.openssl.org/3.0/man5/x509v3_config/", "https://www.rfc-editor.org/rfc/rfc5280#section-4.2.1.13", "https://www.rfc-editor.org/rfc/rfc5280#section-4.2.2.1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AIA and CRL distribution point extensions

## Config
```ini
[ v3_leaf ]
basicConstraints = critical, CA:FALSE
keyUsage = critical, digitalSignature
extendedKeyUsage = serverAuth
authorityInfoAccess = OCSP;URI:http://ocsp.example.com, caIssuers;URI:http://pki.example.com/int.cer
crlDistributionPoints = URI:http://pki.example.com/int.crl
```
- Put these in the profile used by the issuing CA; URLs describe the issuer (the CA that signed this cert).
- Use `http://`, not `https://`: fetching revocation data over TLS can recurse into revocation checking. CRLs and
  OCSP responses are signed already.
- RFC 5280 (4.2.2.1): caIssuers must point to a single DER certificate or a BER/DER "certs-only" CMS message. Servers
  should send `application/pkix-cert` for the certificate and `application/pkcs7-mime` for the certs-only message.
  A CRL URI must point to a single DER CRL and should be served as `application/pkix-crl` (4.2.1.13).

## Root CAs
Roots usually omit AIA and CDP. Intermediates carry the root's CRL URL in their CDP.

## Inspect and test
```sh
openssl x509 -in leaf.pem -noout -ext authorityInfoAccess,crlDistributionPoints
curl -sI http://pki.example.com/int.crl
openssl crl -inform DER -in int.crl -noout -nextupdate
openssl ocsp -issuer int.pem -cert leaf.pem -url http://ocsp.example.com -resp_text
```
All four commands were run against a test CA (OpenSSL 3.2.3; the OCSP query used a local `openssl ocsp -port` responder
and printed `Cert Status: good`).

## Pitfalls
- URLs reachable only internally while certificates are used externally.
- Changing URLs requires reissuing certificates; choose stable hostnames.
- Do not rely on clients fetching missing intermediates through caIssuers; serve the full chain.

## Verify
- [ ] All AIA/CDP URLs return 200 from a client network; CRL is current.
