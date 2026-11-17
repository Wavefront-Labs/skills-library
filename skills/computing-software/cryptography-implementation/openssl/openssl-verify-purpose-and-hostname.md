---
id: computing-software.cryptography-implementation.openssl.openssl-verify-purpose-and-hostname
name: openssl-verify-purpose-and-hostname
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, chain-verification, openssl-verify, verify-purpose, verify-hostname, extended-key-usage, x509-strict, verify-ip, x509]
level: practitioner
status: verified
description: "Make openssl verify check what clients check: -purpose sslserver/sslclient/smimesign, -verify_hostname/-verify_ip, -x509_strict, and checking EKU and key usage explicitly."
sources: ["https://docs.openssl.org/master/man1/openssl-verification-options/", "https://docs.openssl.org/master/man3/X509_check_host/", "https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12", "https://datatracker.ietf.org/doc/html/rfc9525"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# openssl verify: purpose and hostname checks

A chain that verifies may still be unusable: wrong extended key usage (EKU),
wrong name, or a CA certificate used as a server certificate. Add the checks
real clients perform.

```bash
openssl verify -CAfile root.pem -untrusted inter.pem \
  -purpose sslserver -verify_hostname www.example.com -x509_strict leaf.pem
```

## Purpose

`-purpose` checks EKU, key usage and basic constraints for a role:

| `-purpose` | Requires |
|---|---|
| `sslserver` | any EKU present must allow serverAuth; target keyUsage must allow digitalSignature, keyEncipherment and/or keyAgreement |
| `sslclient` | any EKU present must allow clientAuth (mTLS client certs); target keyUsage must allow digitalSignature and/or keyAgreement |
| `smimesign` / `smimeencrypt` | any EKU present must allow emailProtection; keyUsage digitalSignature or nonRepudiation / keyEncipherment |
| `crlsign` | target keyUsage must allow cRLSign |
| `timestampsign` | keyUsage (if present) limited to digitalSignature/nonRepudiation; EKU must be present, critical, timeStamping only |
| `codesign` | keyUsage present, critical, with digitalSignature; EKU must contain codeSign |
| `ocsphelper` | no checks at this stage (special checks apply, see OCSP_basic_verify(3)) |
| `any` | any purpose is accepted |

Failure: `error 26 ... unsuitable certificate purpose`. A classic case:
using a server certificate (serverAuth only) as an mTLS client certificate.

## Names

- `-verify_hostname www.example.com`: matches against the SAN DNS names (the manual says SAN or CN; the underlying
  `X509_check_host` checks the subject CN only if asked to and does not fall back by default, so always use SANs).
  By default a wildcard matches only in the left-most label (`*.example.com` matches `www.example.com`, not
  `a.b.example.com`).
- `-verify_ip 192.0.2.10`: matches SAN iPAddress entries; an IP in a dNSName
  SAN does not count.
- `-verify_email`: the email in the SAN, or in the subject DN.

Failure: `error 62 ... hostname mismatch` / `error 64 ... IP address mismatch`.

## Strictness

`-x509_strict` disables workarounds for broken certificates, so errors are thrown on certificates not compliant with
RFC 5280. Among the checks listed in the manual: CA certificates must include keyUsage, a pathLenConstraint needs
keyCertSign and must not appear on non-CA certificates, issuer names must not be empty, the authorityKeyIdentifier
must be present on X.509v3 certificates unless apparently self-signed, and the subjectKeyIdentifier must be present on
all CA certificates.

## Inspect directly

```bash
openssl x509 -in leaf.pem -noout -ext subjectAltName,extendedKeyUsage,keyUsage,basicConstraints
```

## Verify

- [ ] Server certificates verified with `-purpose sslserver` and every served hostname.
- [ ] mTLS client certs verified with `-purpose sslclient`.
- [ ] Private CA issuance tested with `-x509_strict`.

## Checked

2026-10-26, against the OpenSSL documentation tree (master, 4.1 series; man pages at docs.openssl.org). Confirmed in openssl-verification-options(1) (purpose list and per-purpose checks, `-verify_hostname`, `-verify_ip`, `-verify_email`, `-x509_strict` checks) and X509_check_host(3) (wildcard matching, CN only with an explicit flag, IP addresses in DNS names ignored); error numbers 26, 62 and 64 against include/openssl/x509_vfy.h. Fixed the purpose table (crlsign and ocsphelper do not use an EKU) and removed unconfirmed claims about Go, Java and the CN.

2026-11-01, run with OpenSSL 3.2.3 against a throwaway root, intermediate and server certificate (SAN DNS and IP, serverAuth only) in a temp directory. Confirmed: the full example command succeeds; `-purpose sslclient`, `crlsign`, `smimesign`, `codesign` and `timestampsign` fail with error 26 on that serverAuth-only leaf while `any` and `ocsphelper` pass; a CA certificate fails `-purpose sslserver` (26); `-verify_hostname` mismatch is error 62; `-verify_ip` mismatch is error 64, also for an IP placed in a dNSName SAN; `-verify_email` matches a SAN email and mismatch is error 63; a `*.example.com` SAN matches `www.example.com` but not `a.b.example.com`; `-x509_strict` rejects a CA without keyUsage (error 92) that plain verify accepts; `openssl x509 -noout -ext` prints the listed extensions.

Method: documentation checked, then the commands were run as above (OpenSSL 3.2.3, local files only).
