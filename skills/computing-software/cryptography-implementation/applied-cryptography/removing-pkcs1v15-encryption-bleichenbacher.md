---
id: computing-software.cryptography-implementation.applied-cryptography.removing-pkcs1v15-encryption-bleichenbacher
name: removing-pkcs1v15-encryption-bleichenbacher
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, rsa-oaep, bleichenbacher, pkcs1v15, robot-attack, marvin-attack, implicit-rejection, rsa-encryption, tls-rsa-key-exchange]
level: sme
status: docs-checked
description: "Find and remove RSA PKCS#1 v1.5 encryption (Bleichenbacher/ROBOT/Marvin oracles), and use implicit rejection when it cannot yet be removed."
sources: ["https://robotattack.org/", "https://people.redhat.com/~hkario/marvin/", "https://datatracker.ietf.org/doc/draft-irtf-cfrg-rsa-guidance/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Removing PKCS#1 v1.5 encryption

Bleichenbacher (1998): if a server reveals whether an RSA ciphertext has valid PKCS#1 v1.5
padding (via an error, alert or timing), an attacker can perform RSA decryption and signing
operations with the server's private key. It returns every few years: ROBOT (2017, TLS RSA
encryption key exchange; vulnerable implementations from at least seven vendors including F5,
Citrix and Cisco) and Marvin (a timing variant). The Marvin page lists affected implementations
including BouncyCastle, GnuTLS, Go, Java, libgcrypt, Mbed, Node, NSS, OpenSSL, pyca/cryptography,
Python, Ruby, Rust OpenSSL and a Wolf entry. The attack does not recover the private key, so
a vulnerable server need not revoke its certificate (ROBOT FAQ), but it should be fixed.

## Where it hides
- TLS cipher suites using RSA encryption key exchange (ROBOT: only servers that enable RSA
  encryption are affected; suites using RSA signatures with DHE or ECDHE are not).
- Application code calling an RSA decrypt API with PKCS#1 v1.5 padding selected or defaulted:
  search your code for the padding constant your library uses for it.
- The RSA guidance draft's scope: RSAES-PKCS1-v1_5 is the encryption scheme; RSA signatures with
  PKCS#1 v1.5 padding are a different scheme and not the subject here.

## Remediation order
1. TLS: disable cipher suites that use RSA encryption; most modern clients support ECDH, which
   is the recommended fix. Older clients can use finite-field DH, secure only with fresh DHE key
   shares per connection (protection against Raccoon) and well-known safe-prime parameters.
2. Application code: migrate to RSA-OAEP (self-verifying padding) or another scheme, and version
   the format.
3. The RSA guidance draft (draft-irtf-cfrg-rsa-guidance) says RSAES-PKCS-v1_5 is deprecated, should
   be used only to process legacy data, and MUST NOT be used as part of online protocols or API
   endpoints.

## If you cannot remove it yet
- Implement implicit rejection exactly as specified in the draft (section 7): on a failed padding
  check, return a deterministic pseudo-random message derived from the private key and the
  ciphertext, so the caller cannot tell whether the check failed; only publicly invalid
  ciphertexts (value larger than the modulus, wrong length) return errors. It MUST be implemented as
  stated, because two implementations sharing a key but rejecting differently let an attacker
  compare behaviour.
- Prefer constant-time big-number code; the Marvin page notes that default bignum modes of
  common libraries are not constant time and links constant-time alternatives.

## Verify
- [ ] No cipher suites using RSA encryption key exchange are offered; scan with the ROBOT
      detection tool (robot-detect, linked from robotattack.org).
- [ ] No remaining PKCS#1 v1.5 decrypt call sites except legacy-data batch jobs.

## Checked
Method: docs-checked 2026-11-09 against robotattack.org (summary, FAQ and mitigation sections), the Marvin page at people.redhat.com (affected list and "What should I do?") and draft-irtf-cfrg-rsa-guidance-06 (section 7 implicit rejection, deprecation text). Removed unconfirmed claims about OpenSSL 3.2 defaults, specific API names, JWE and XML identifiers, TLS 1.3 and testssl and Wycheproof vectors; the Bleichenbacher 1998 PDF was not read.
