---
id: computing-software.cryptography-implementation.openssl.extracting-public-keys-and-raw-key-bytes
name: extracting-public-keys-and-raw-key-bytes
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, pubout, openssl-pkey, public-key, raw-keys, ed25519, x25519, ec-point, spki-hash, key-inspection]
level: practitioner
status: verified
description: "Extract public keys with openssl pkey -pubout, dump raw Ed25519/X25519 bytes and EC points, convert compressed points, and hash SPKI for pinning."
sources: ["https://docs.openssl.org/3.0/man1/openssl-pkey/", "https://docs.openssl.org/3.0/man1/openssl-ec/", "https://www.rfc-editor.org/rfc/rfc8410"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extracting public keys and raw key bytes

## Public key from a private key, CSR or certificate
```
openssl pkey -in key.pem -pubout -out pub.pem
openssl req  -in req.csr  -noout -pubkey > pub.pem
openssl x509 -in cert.pem -noout -pubkey > pub.pem
openssl pkey -pubin -in pub.pem -text -noout        # human-readable
```

## Raw bytes for Ed25519 / X25519 (RFC 8410 encodings)
The DER SubjectPublicKeyInfo for these keys is a fixed 12-byte prefix plus the 32-byte key; the PKCS#8 private key
is a fixed 16-byte prefix plus the 32-byte seed.
```
openssl pkey -in ed.pem -pubout -outform DER | tail -c 32 | xxd -p -c 32     # raw public key
openssl pkey -in ed.pem -outform DER | tail -c 32 | xxd -p -c 32             # raw private seed (handle as secret)
```
OpenSSL 3 can also print them: `openssl pkey -in ed.pem -text -noout` shows `priv:` and `pub:` hex blocks.
Going the other way (raw 32 bytes to PEM): prepend the DER prefix `302a300506032b6570032100` for an Ed25519 public
key (`302a300506032b656e032100` for X25519) and convert with `openssl pkey -pubin -inform DER`.

## EC public points
```
openssl pkey -pubin -in ecpub.pem -text -noout              # 04 || X || Y uncompressed point
openssl ec -pubin -in ecpub.pem -conv_form compressed -outform DER -out ecpub-c.der
```
Some peers (smart cards, blockchains) need compressed 33-byte points; X.509 normally uses uncompressed.

## SPKI hash for pinning and matching
```
openssl pkey -pubin -in pub.pem -outform DER | openssl dgst -sha256 -binary | base64
```
This is the value used by HPKP-style pins, SSH-like fingerprints for TLS keys, and certificate/key matching.

## Gotchas
- Tested on OpenSSL 3.2.3: DER SPKI prefix `302a300506032b6570032100` (Ed25519) and `302a300506032b656e032100` (X25519)
  are 12 bytes; the PKCS#8 private prefix `302e020100300506032b657004220420` is 16 bytes; Ed448 public DER is 69 bytes and
  private 73; X448 public 68. Raw bytes plus the prefix round-tripped to an identical PEM.
- `tail -c 32` tricks only work for fixed-length encodings (Ed25519, X25519, Ed448 uses 57 bytes, X448 56);
  never for RSA or EC private keys.
- `openssl rsa -pubout` and `openssl ec -pubout` are legacy per-algorithm forms; `pkey` covers all types.
- Writing raw private seeds to files bypasses PEM encryption; keep them in memory or encrypted.

## Verify
- [ ] Raw public key round-trips back to an identical PEM.
- [ ] SPKI hash from key, CSR and certificate are equal.
