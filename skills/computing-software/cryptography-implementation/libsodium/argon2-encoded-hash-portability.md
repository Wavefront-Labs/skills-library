---
id: computing-software.cryptography-implementation.libsodium.argon2-encoded-hash-portability
name: argon2-encoded-hash-portability
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, argon2-encoded-hash, argon2id, crypto-pwhash-str, phc-string-format, libsodium, argon2-cffi, password-hash-migration, interop]
level: practitioner
status: verified
description: "Move Argon2id password hashes between libsodium, argon2-cffi, PHP and Go: PHC encoded string fields, parallelism limits, buffer sizes and verification tests."
sources: ["https://doc.libsodium.org/password_hashing/default_phf", "https://github.com/P-H-C/phc-string-format/blob/master/phc-sf-spec.md", "https://www.rfc-editor.org/rfc/rfc9106", "https://www.php.net/manual/en/function.password-hash.php", "https://pkg.go.dev/golang.org/x/crypto/argon2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argon2 encoded hash portability

## The string
```
$argon2id$v=19$m=65536,t=2,p=1$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG
   alg     ver  memory KiB, iterations, lanes   salt (b64, no padding)   tag (b64, no padding)
```
libsodium `crypto_pwhash_str` writes this format (NUL-terminated, buffer `crypto_pwhash_STRBYTES` = 128) and
`crypto_pwhash_str_verify` reads parameters from it, so old hashes verify after you raise defaults.

## Library differences
| Library | Notes |
|---|---|
| libsodium | Produces `p=1`; `opslimit` maps to `t`, `memlimit` bytes maps to `m` (KiB): INTERACTIVE gives `m=65536,t=2,p=1` (run on libsodium 1.0.22 via libsodium.js and PyNaCl 1.6.2) |
| argon2-cffi (Python) | Defaults `m=65536,t=3,p=4` (run on the installed release); verifies libsodium's `p=1` strings, and libsodium verified its `p=4` string |
| PHP `password_hash(PASSWORD_ARGON2ID)` | Built against libargon2 or libsodium; the `threads` option (sets p) is only available with libargon2, not the libsodium implementation (PHP manual) |
| Go `golang.org/x/crypto/argon2` | Raw functions only (`IDKey`, `Key`); you build and parse the PHC string yourself |
| Node `argon2` package | PHC strings, `parallelism` default 4 (package wiki) |

Hashes created with `p > 1` must be verified by an implementation that supports multiple lanes (libsodium does: it verified an argon2-cffi `p=4` string). Test a sample of real
hashes in the target library before migrating; do not assume.

## Migration recipe
1. Collect a few hashes per parameter set from production (with test passwords you control in staging).
2. Verify them with the target library; fix parsing (padding, base64 alphabet) if needed.
3. Switch verification; keep `needs_rehash` logic so hashes upgrade to the new defaults on login.

## Gotchas
- Base64 here is unpadded standard alphabet; some custom parsers expect URL-safe or padded.
- Truncating the string on storage (VARCHAR(64)) corrupts it; allow at least 128 characters.
- Argon2i (not id) strings from libsodium (`$argon2i$...`) still verify with the generic verify call (tested); rehash them to id.

## Verify
- [ ] Cross-library verification test passes for every parameter set in production.
- [ ] Column width >= 128.
