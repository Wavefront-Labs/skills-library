---
id: computing-software.cryptography-implementation.libsodium.pwhash-str-storage-and-verification
name: pwhash-str-storage-and-verification
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-pwhash, pwhash-str, crypto-pwhash-str-verify, argon2id, password-storage, phc-string-format, login-flow]
level: practitioner
status: docs-checked
description: "Store and verify passwords with crypto_pwhash_str/_str_verify: the $argon2id$ string, buffer sizes, login flow, and interop with other Argon2 libraries."
sources: ["https://doc.libsodium.org/password_hashing/default_phf", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/include/sodium/crypto_pwhash_argon2id.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_pwhash_str: password storage and verification

`crypto_pwhash_str` hashes a password with Argon2id, a random salt and the
given limits, and returns a self-describing ASCII string to store as-is.

```c
char hash[crypto_pwhash_STRBYTES];                       /* 128, includes NUL */
if (crypto_pwhash_str(hash, pw, strlen(pw),
        crypto_pwhash_OPSLIMIT_MODERATE, crypto_pwhash_MEMLIMIT_MODERATE) != 0) {
    /* out of memory: do not store anything */
}
/* store `hash` (e.g. VARCHAR(128)) */

if (crypto_pwhash_str_verify(hash_from_db, pw, strlen(pw)) != 0) {
    /* wrong password (or malformed hash) */
}
```

The string starts with `$argon2id$` (`crypto_pwhash_STRPREFIX`) and, per the docs, includes the salt, the algorithm identifier and version, `opslimit` and `memlimit`, so verification needs nothing else. For MODERATE limits (opslimit 3, 256 MiB) the parameter field reads `m=262144,t=3`.

## Login flow

1. Look up the user; if absent, still run a verify against a dummy hash (same
   parameters) so response time does not reveal which usernames exist.
2. `crypto_pwhash_str_verify`; on success, call
   `crypto_pwhash_str_needs_rehash(hash, opslimit, memlimit)` and re-hash with
   current limits if it returns 1 (it returns 0 when the parameters match and -1 on error).
3. Rate-limit attempts per account and per IP; Argon2id cost also limits
   throughput, so size worker pools (MODERATE uses 256 MiB per hash).

## Interop

`crypto_pwhash_str` uses the current default algorithm, which is Argon2id since libsodium 1.0.15. Before moving verification to another stack, test that library against hashes produced by libsodium.

## Gotchas

- Pass the password length explicitly; passwords may contain NUL bytes in
  some encodings - decide on UTF-8 and a Unicode normalisation form first.
- `crypto_pwhash_str` can fail under memory pressure: handle -1 and never
  store a partial buffer.
- Do not truncate the stored string; reserve `crypto_pwhash_STRBYTES` (128) bytes. The string is zero-terminated and may be shorter.

## Verify

- [ ] Stored hashes begin with `$argon2id$` and include current parameters.
- [ ] Unknown-user path runs a dummy verify.
- [ ] Rehash-on-login implemented with `needs_rehash`.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: crypto_pwhash_str and _str_verify signatures and return values, STRBYTES 128 and the zero-terminated ASCII output including salt, algorithm, version and limits, the $argon2id$ prefix, needs_rehash return values, Argon2id as default since 1.0.15, MODERATE limits (opslimit 3, 256 MiB, so m=262144). Removed unconfirmed interoperability claims with argon2-cffi, PHP password_hash and the Rust argon2 crate, and the PHC and RFC 9106 source entries.

Method: documentation only; no commands were run.
