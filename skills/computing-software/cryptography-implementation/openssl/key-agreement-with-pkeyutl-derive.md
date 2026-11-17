---
id: computing-software.cryptography-implementation.openssl.key-agreement-with-pkeyutl-derive
name: key-agreement-with-pkeyutl-derive
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, pkeyutl-derive, pkeyutl, ecdh, x25519, openssl-kdf, hkdf, key-agreement, testing]
level: practitioner
status: verified
description: "Derive ECDH and X25519 shared secrets with openssl pkeyutl -derive, post-process them with openssl kdf HKDF, and use the result for scripted tests."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkeyutl/", "https://docs.openssl.org/3.0/man1/openssl-kdf/", "https://www.rfc-editor.org/rfc/rfc7748"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key agreement with pkeyutl -derive

## X25519
```
openssl genpkey -algorithm X25519 -out alice.key && openssl pkey -in alice.key -pubout -out alice.pub
openssl genpkey -algorithm X25519 -out bob.key   && openssl pkey -in bob.key -pubout -out bob.pub
openssl pkeyutl -derive -inkey alice.key -peerkey bob.pub -out z_alice.bin
openssl pkeyutl -derive -inkey bob.key -peerkey alice.pub -out z_bob.bin
cmp z_alice.bin z_bob.bin && xxd -p -c 32 z_alice.bin
```

## ECDH on P-256
```
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out a.key
openssl pkey -in a.key -pubout -out a.pub
openssl pkeyutl -derive -inkey a.key -peerkey b.pub -out z.bin    # 32-byte x-coordinate
```
Peer key must use the same curve. With `-pkeyopt ecdh_cofactor_mode:1` you get cofactor ECDH (no effect on P-256,
cofactor 1).

## Never use Z directly: run a KDF
```
openssl kdf -keylen 32 -kdfopt digest:SHA256 -kdfopt hexkey:$(xxd -p -c 256 z.bin) \
  -kdfopt salt:session-salt -kdfopt info:example-v1-enc -binary HKDF > enc.key
```
`-kdfopt mode:EXPAND_ONLY` / `EXTRACT_ONLY` select HKDF steps; `SSKDF` and `X963KDF` are the SP 800-56C and X9.63
alternatives.

## KEMs (OpenSSL 3.5+)
`pkeyutl -encap` / `-decap` (listed in the 3.5 manual, with `-kemop`) produce a shared secret and ciphertext instead of
`-derive`. Not run here (OpenSSL 3.2.3 has no `-encap`).

## Uses
- Producing test vectors to compare against your application's key agreement.
- Debugging interop: derive Z with OpenSSL from both sides' keys and compare with the app's value.

## Gotchas
- Derived secrets written to files are secrets; use a tmpfs and delete them.
- OpenSSL 3.2.3 rejects an all-zero X25519 peer key (`failed during derivation`); older versions may not, so check in
  tests. A peer key on a different curve fails with `mismatching domain parameters`.

## Verify
- [ ] Both sides produce identical Z.
- [ ] KDF output matches your application's derived key for the same inputs.
