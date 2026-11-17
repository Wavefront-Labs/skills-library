---
id: computing-software.cryptography-implementation.crypto-libraries.kdf-parameter-interop-across-languages
name: kdf-parameter-interop-across-languages
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, kdf-parameter-interop, pbkdf2, scrypt, argon2, hkdf, cross-language]
level: practitioner
status: verified
description: "Match PBKDF2, scrypt, Argon2 and HKDF parameters across languages: iteration and memory units, password encoding, salt and info bytes, output length, and test vectors."
sources: ["https://www.rfc-editor.org/rfc/rfc8018", "https://www.rfc-editor.org/rfc/rfc7914", "https://www.rfc-editor.org/rfc/rfc9106", "https://docs.rs/scrypt/latest/scrypt/struct.Params.html", "https://nodejs.org/api/crypto.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KDF parameter interop across languages

## Units that differ
| KDF | Parameter | Gotcha |
|---|---|---|
| PBKDF2 | key length | Python `hashlib.pbkdf2_hmac`, Node `pbkdf2Sync` and Go take bytes (32 gave 32 bytes, run); Java `PBEKeySpec` `keyLength` is in bits (Java 8: 256 gave a 32-byte key with the same PBKDF2-HMAC-SHA256 output as Python and Node, `...a38253555ce37f5c`) |
| PBKDF2 | PRF | name the hash explicitly (`sha256` in Python/Node, `PBKDF2WithHmacSHA256` in Java); do not rely on a default |
| scrypt | N | Rust `scrypt::Params::new(log_n, r, p)` takes log2(N) (`LOG_N` 17 = N 131072); Node `{N: 131072}` and Python `n=131072` take N |
| scrypt | memory cap | Node (`ERR_CRYPTO_INVALID_SCRYPT_PARAMS ... memory limit exceeded`) and Python (`ValueError ... memory limit exceeded`) both reject N=2^17, r=8, p=1 with the default `maxmem` (about 32 MiB) until `maxmem` is raised (256 MiB worked and both gave the same key `8e489c9f...`) |
| Argon2 | memory | libsodium/PyNaCl `memlimit` in bytes (`MEMLIMIT_INTERACTIVE` = 67108864); argon2-cffi `memory_cost` and PHC strings in KiB (`m=65536`; PyNaCl's own PHC output also says `m=65536`) |
| Argon2 | version | 0x13 (19) vs 0x10 (16) give different output for the same inputs (argon2-cffi, `ID`, 1 MiB: `f9c23e91...` vs `aa159eff...`); variant id vs i vs d also differs |
| HKDF | salt absent | RFC 5869: HashLen zeros. pyca (`None`, `b""`, 32 zero bytes), Node `hkdfSync` (`""` and 32 zero bytes) and Go (`nil` and 32 zero bytes) each gave identical output |

## Encoding
- Password bytes: UTF-8 everywhere; the `PBEKeySpec` Javadoc says different PBE mechanisms consume different bits of each password
  char (PKCS #5 looks at the low order 8 bits, PKCS #12 all 16). Normalise Unicode (NFC or NFKC) before hashing if users type on varied keyboards.
- Salts and info: pass raw bytes, not hex strings; `"00ff"` hex and bytes `00 ff` give different keys (PBKDF2, checked in Python).

## Record parameters
Store a self-describing string: PHC format `$argon2id$v=19$m=65536,t=3,p=4$salt$hash` (argon2-cffi `PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4).hash()` produced exactly that prefix) or a JSON header with
`kdf`, `params`, `salt` (base64). Never rely on library defaults, which change between versions.

## Verify
- [ ] Shared golden vector (password, salt, params, expected output) checked in every language's tests.
