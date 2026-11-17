---
id: computing-software.cryptography-implementation.secure-implementation.rejecting-weak-peer-parameters
name: rejecting-weak-peer-parameters
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, weak-parameter-rejection, input-validation, logjam, minimum-key-size, downgrade]
level: practitioner
status: docs-checked
description: "Reject weak parameters supplied by peers: small DH groups, short RSA keys, low KDF cost parameters, weak curves and downgraded algorithms in received messages."
sources: ["https://weakdh.org/", "https://docs.openssl.org/3.0/man3/SSL_CTX_set_security_level/", "https://www.rfc-editor.org/rfc/rfc7919"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rejecting weak peer parameters

Any parameter chosen by the other side is attacker-controlled until validated.

## What to enforce
| Parameter | Rule |
|---|---|
| Finite-field DH group | servers use 2048-bit or larger primes; clients reject small primes; prefer RFC 7919 named groups |
| RSA, DSA, DH keys | enforce a minimum size through your library's security level |
| EC curves | accept only curves from an allow list; reject explicit curve parameters |
| Signature hashes | reject signatures with hashes your policy no longer accepts |
| KDF cost parameters in received files | set lower and upper bounds (too low = weak, too high = DoS) |
| JWT/JWE `alg`, `enc` | allow list |

## Implementation
- OpenSSL security level (`SSL_CTX_set_security_level`): level 2 is 112 bits of security and prohibits RSA, DSA
  and DH keys shorter than 2048 bits; level 3 is 128 bits and prohibits keys shorter than 3072 bits. Setting
  certificates or parameters that fail the level is blocked.
- Parsing your own formats: validate params before running the KDF or decryption.

## Logjam lesson
Services that support DHE_EXPORT cipher suites are at risk of the Logjam attack. The Logjam authors advise
disabling export suites, using 2048-bit or larger primes on servers, and having clients reject DH primes
smaller than 1024 bits. Clients must reject small groups even when the server offers them.

## Verify
- [ ] Negative tests: undersized RSA cert, undersized DH group, explicit-curve key, KDF cost of 1 are all rejected.

## Checked

Date: 2026-11-01. Confirmed in the OpenSSL SSL_CTX_set_security_level manual (levels 2 and 3, key size exclusions, blocked certificate setting) and the weakdh.org Logjam page (DHE_EXPORT risk, 2048-bit primes, clients reject primes under 1024 bits). RFC 7919 is cited for named finite-field groups. Removed: the minimum table figures not in these pages (e = 65537, curve names, SHA-256, TLS 1.2), Java property names and the Go behaviour.
Method: documentation only; no commands were run.
