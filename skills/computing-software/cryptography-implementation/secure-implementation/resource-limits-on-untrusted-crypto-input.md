---
id: computing-software.cryptography-implementation.secure-implementation.resource-limits-on-untrusted-crypto-input
name: resource-limits-on-untrusted-crypto-input
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, point-validation, crypto-dos-limits, denial-of-service, decompression-bomb, rate-limiting]
level: practitioner
status: docs-checked
description: "Cap CPU and memory spent on untrusted crypto input: key sizes, KDF cost from headers, chain and token limits, decompression bombs, and verify-before-expensive-work."
sources: ["https://www.rfc-editor.org/rfc/rfc8725.txt", "https://www.rfc-editor.org/rfc/rfc7518.txt", "https://www.openssl.org/news/secadv/20230731.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource limits on untrusted crypto input

Crypto is expensive by design. If an attacker controls the parameters, they control your CPU.
The caps below are deployment choices: pick a number for your workload, enforce it in code and document it.

## Attacker-controlled cost parameters
| Input | Attack | Limit |
|---|---|---|
| RSA public key in a cert/JWK | very large modulus makes verify slow; huge exponent `e` | maximum modulus size you accept; `e` fixed or small |
| DH parameters (peer-supplied `p`/`q`, PEM files) | very large values make `DH_check()` slow (OpenSSL CVE-2023-3817, an earlier fix was CVE-2023-3446) | fixed named groups (RFC 7919), cap on bits; avoid `DH_check` on untrusted input |
| JWE PBES2 `p2c` header | attacker-chosen PBKDF2 iteration count | cap `p2c` or disable PBES2 on untrusted tokens |
| Password hash string from a DB/import (`$argon2id$m=...`) | huge memory cost `m` | enforce max m, t, p on parse |
| Certificate chain | very long chains, name-constraint explosion | depth cap, total size cap, verification time budget |
| JWT/JWS | very large tokens, many JWS signatures | max token size, single signature |
| Compressed payloads (compressed JWE, CMS, zip) | decompression bomb | cap decompressed size and ratio; or refuse compression |

RFC 8725 section 3.6 says compression of data SHOULD NOT be done before encryption, since compressed data often
reveals information about the plaintext.

## Order of operations
1. Cheap checks first: size caps, format, algorithm allowlist.
2. Authenticate before expensive or dangerous work: verify the MAC/signature before
   decompressing, deserialising or running a slow KDF where possible.
3. For unauthenticated expensive steps (password login, signature verify on public endpoints),
   rate limit per client and globally, and run them on a bounded worker pool so a flood cannot
   starve other requests.

## Memory-hard KDF capacity
Argon2id with m=64 MiB means 100 concurrent logins need 6400 MiB. Size a semaphore to memory, queue
the rest, and shed load with 429 rather than OOM-killing the process.

## Streaming input
Limit read size before parsing; never read an upload fully into memory and then decrypt. Use chunked
streaming AEAD for large files and still cap total size.

## Verify
- [ ] Tests send oversize keys, huge `p2c`, oversized tokens and bombs; each is rejected quickly.
- [ ] Load test of the login endpoint shows bounded memory and 429 under flood.
- [ ] Limits are configuration with safe defaults, documented next to the parser.

## Checked

2026-10-31. Confirmed: OpenSSL advisory of 31 July 2023 (CVE-2023-3817: `DH_check()`, `DH_check_ex()`,
`EVP_PKEY_param_check()` and `dhparam`/`pkeyparam -check` can be very slow on untrusted DH values; it refers to the
earlier fix CVE-2023-3446; the TLS implementation is not affected), RFC 7518 section 4.8.1.2 (`p2c` is the PBKDF2
iteration count, chosen by the sender of the header), RFC 8725 section 3.6 (SHOULD NOT compress before encryption).
Corrected: the DH_check slowness is CVE-2023-3817 (the old text named only CVE-2023-3446); 100 x 64 MiB is 6400 MiB, not
"6.4 GiB". Removed (no source read): the specific numeric caps (4096/8192-bit moduli, 600000 `p2c`, depth 10, 8 KiB
tokens), "Go 1.24+ caps RSA keys", `http.MaxBytesReader` and `client_max_body_size`, and the RFC 7919 8192-bit statement.
Method: documentation only; no commands were run.
