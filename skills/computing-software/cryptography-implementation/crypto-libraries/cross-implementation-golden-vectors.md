---
id: computing-software.cryptography-implementation.crypto-libraries.cross-implementation-golden-vectors
name: cross-implementation-golden-vectors
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, interop-golden-vectors, test-vectors, cross-language, interop-testing, wycheproof]
level: practitioner
status: verified
description: "Build and maintain golden test vectors shared across implementations: generating with a reference, JSON format, covering edge cases, and running in every language CI."
sources: ["https://github.com/C2SP/wycheproof", "https://github.com/C2SP/CCTV", "https://www.rfc-editor.org/rfc/rfc8439#appendix-A", "https://github.com/C2SP/wycheproof/blob/main/testvectors_v1/aes_gcm_test.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-implementation golden vectors

When a format or protocol is implemented in several languages (server Go, client Swift/Kotlin/JS), a shared vector
file is the cheapest guard against silent incompatibility.

## Build the file
- Generate from a reference implementation with fixed inputs (keys, nonces, plaintexts), never random at test
  time.
- JSON with hex or base64 fields plus a `comment` and `result` like Wycheproof. The real Wycheproof `aes_gcm_test.json` has
  top-level `algorithm`, `schema`, `numberOfTests`, `header`, `notes`, `testGroups`; each group has `ivSize`, `keySize`, `tagSize`,
  `type` and `tests`; each test has `tcId`, `comment`, `flags`, `key`, `iv`, `aad`, `msg`, `ct`, `tag`, `result` (so `iv`/`msg`, not
  `nonce`/`pt`, and the tag is a separate field; that file has 229 `valid` and 87 `invalid` cases and no `acceptable` ones; the
  schema allows `acceptable` for other algorithms, so decide how your harness treats it). Your own format, in the same spirit:
  ```json
  {"algorithm":"myformat-v2","tests":[
    {"tcId":1,"comment":"empty plaintext","key":"00..1f","nonce":"...","aad":"","pt":"","ct":"...","result":"valid"},
    {"tcId":2,"comment":"tag bit flipped","key":"...","ct":"...","result":"invalid"}]}
  ```
- Cover: empty input, block-boundary lengths (15, 16, 17, 4096 bytes), maximum sizes, Unicode passwords, leading
  zero integers, every version of the format, and invalid cases (truncated, wrong version, tampered).

## Use it
- Store in a shared repo or package; each implementation's CI downloads a pinned version and runs all cases.
- Add a vector for every interop bug found before fixing it.
- Check primitives too: include RFC/NIST/Wycheproof vectors for the underlying algorithms. Run here: the RFC 8439 Appendix A.5
  ChaCha20-Poly1305 decryption vector (265-byte ciphertext, 12-byte nonce, 12-byte AAD, 16-byte tag, parsed from the RFC text)
  decrypted to `Internet-Drafts are draft documents...` with pyca `cryptography` 50.0.2, and flipping one ciphertext byte raised
  `InvalidTag`; of the Wycheproof AES-GCM cases with a 96-bit IV and 128-bit tag, all 197 agreed with pyca `AESGCM` (valid cases
  decrypt, invalid cases fail), and the other 119 cases use other IV or tag sizes that `AESGCM` does not take.

## Pitfalls
- Regenerating vectors from the code under test after a change (it then always passes). Treat vectors as
  append-only; new behaviour gets a new version.

## Verify
- [ ] All implementations report the same pass/fail per tcId; CI fails on any mismatch.
