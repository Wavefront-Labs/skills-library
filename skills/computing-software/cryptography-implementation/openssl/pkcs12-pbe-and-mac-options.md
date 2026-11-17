---
id: computing-software.cryptography-implementation.openssl.pkcs12-pbe-and-mac-options
name: pkcs12-pbe-and-mac-options
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, pkcs12-pbe, pkcs12, pfx, pbes2, pbkdf2, pbmac1, openssl-pkcs12, keystore]
level: practitioner
status: verified
description: "Control PKCS#12 encryption and integrity in OpenSSL: -keypbe, -certpbe, -macalg, -iter, -maciter, PBMAC1, and choosing settings per consumer."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkcs12/", "https://www.rfc-editor.org/rfc/rfc7292", "https://www.rfc-editor.org/rfc/rfc9579"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKCS#12 PBE and MAC options

A PKCS#12 file has two password-based layers: encryption of the key and certificate bags (PBE), and an outer
integrity MAC.

## OpenSSL 3 defaults
- Key and cert bags: PBES2 with PBKDF2-HMAC-SHA256 and AES-256-CBC, 2048 iterations.
- MAC: HMAC-SHA256, 2048 iterations.

## Options
```
openssl pkcs12 -export -inkey key.pem -in cert.pem -certfile chain.pem -out out.p12 \
  -keypbe AES-256-CBC -certpbe AES-256-CBC -macalg sha256 -iter 100000 -maciter
```
| Option | Effect |
|---|---|
| `-keypbe ALG` / `-certpbe ALG` | Cipher for key bag / cert bag (`NONE` for certpbe leaves certificates unencrypted) |
| `-macalg sha256` | MAC digest |
| `-iter N` | Iteration count for the encryption key and the MAC (default 2048) |
| `-noiter` / `-nomaciter` | Set the encryption / MAC iteration count to 1 (only for broken legacy consumers; tested: `-iter 5000 -nomaciter` gave encryption 5000, MAC 1) |
| `-maciter` | Accepted for compatibility; MAC iterations are on by default |
| `-nomac` | No integrity MAC (`openssl pkcs12 -info` then prints `Warning: MAC is absent!`); the manual says it can help with the FIPS provider because the PKCS#12 MAC needs PKCS12KDF, which is not FIPS-approved |
| `-pbmac1_pbkdf2` | PBMAC1 MAC (RFC 9879, which obsoletes RFC 9579), documented from OpenSSL 3.4 |
| `-legacy` | RC2/3DES with SHA-1 for very old consumers |

## Choosing
| Consumer | Settings |
|---|---|
| Modern consumers | Defaults, raise `-iter` (e.g. 100k+) for files that travel (tested: `-iter 100000` gives MAC and bag counts of 100000) |
| Old consumers that reject AES/SHA-256 | `-keypbe PBE-SHA1-3DES -certpbe PBE-SHA1-3DES -macalg sha1` first, then `-legacy` (RC2/3DES), and treat the file as weakly protected |
| FIPS environments | PBES2 with AES; `-nomac` or PBMAC1 (3.4+) per the manual; check the consumer supports it |

## Gotchas
- The password is the real protection; PKCS#12 iteration counts are low compared to password-hashing guidance, so
  use long random passwords for files that leave a secure host. OpenSSL 3.2.3 defaults tested: PBES2, PBKDF2,
  AES-256-CBC, HMAC-SHA256, 2048 iterations; `-certpbe NONE` leaves certificate bags unencrypted.
- Encrypting cert bags is optional; some tools fail on unencrypted cert bags and vice versa.

## Verify
- [ ] `openssl pkcs12 -info -noout` reports the intended PBE, MAC and iteration counts.
- [ ] The consuming platform imports the file.
