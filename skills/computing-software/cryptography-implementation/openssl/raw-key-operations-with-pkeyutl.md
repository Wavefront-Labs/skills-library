---
id: computing-software.cryptography-implementation.openssl.raw-key-operations-with-pkeyutl
name: raw-key-operations-with-pkeyutl
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, pkeyutl, openssl-dgst, ecdh-derive, rsa-oaep, kem, ml-kem, hsm-debugging, openssl-3]
level: advanced
status: docs-checked
description: "Use openssl pkeyutl for raw public-key operations: RSA-OAEP encrypt/decrypt, signing precomputed digests, ECDH/X25519 derive, ML-KEM encap/decap, and its option syntax."
sources: ["https://docs.openssl.org/3.5/man1/openssl-pkeyutl/", "https://docs.openssl.org/3.0/man7/EVP_PKEY-EC/", "https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw key operations with pkeyutl

`openssl pkeyutl` exposes EVP_PKEY operations directly: encrypt, decrypt,
sign a digest, verify, derive, and (3.5+) KEM encapsulate/decapsulate. Use it
for interop debugging, test vectors and scripting key transport; not for bulk
data.

## RSA-OAEP key transport

```bash
openssl rand -out dek.bin 32
openssl pkeyutl -encrypt -pubin -inkey rsa.pub -in dek.bin -out dek.enc \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256
openssl pkeyutl -decrypt -inkey rsa.key -in dek.enc -out dek.out \
  -pkeyopt rsa_padding_mode:oaep -pkeyopt rsa_oaep_md:sha256 -pkeyopt rsa_mgf1_md:sha256
```

Set `rsa_padding_mode:oaep` explicitly; the other modes are `pkcs1`, `none`, `x931` and `pss`.

## Sign a precomputed digest

```bash
openssl dgst -sha256 -binary data > data.sha256
openssl pkeyutl -sign -inkey ec.key -in data.sha256 -out sig.der -pkeyopt digest:sha256
openssl pkeyutl -verify -pubin -inkey ec.pub -in data.sha256 -sigfile sig.der -pkeyopt digest:sha256
```

For RSA PKCS#1 v1.5 the `digest:` option makes pkeyutl add the DigestInfo to the precomputed digest.

## Key agreement

```bash
openssl pkeyutl -derive -inkey my_x25519.key -peerkey peer_x25519.pub -out shared.bin
openssl pkeyutl -derive -inkey my_p256.key -peerkey peer_p256.pub -out shared.bin
```

The output is the raw shared secret: feed it to a KDF (`openssl kdf HKDF ...`).

## ML-KEM (OpenSSL 3.5+)

```bash
openssl genpkey -algorithm ML-KEM-768 -out kem.key
openssl pkey -in kem.key -pubout -out kem.pub
openssl pkeyutl -encap -pubin -inkey kem.pub -out ct.bin -secret ss_sender.bin
openssl pkeyutl -decap -inkey kem.key -in ct.bin -secret ss_receiver.bin
cmp ss_sender.bin ss_receiver.bin && echo match
```

## Options worth knowing

- `-keyform DER|PEM|P12` selects the key file format.
- `-rawin` treats the input as the message itself rather than a digest.
- `-pkeyopt_passin` for passwords on options; `-passin` for encrypted keys.

## Verify

- [ ] Round trip encrypt/decrypt or encap/decap produces identical bytes.
- [ ] Scripts set `rsa_padding_mode:oaep` explicitly for RSA encryption.

## Checked
2026-11-01. Confirmed in the openssl-pkeyutl man page: `-encrypt`/`-decrypt`/`-sign`/`-verify`/`-derive`, `-encap`/`-decap` with `-secret`, `-pubin`, `-peerkey`, `-sigfile`, `-rawin`, `-pkeyopt_passin`, `-keyform DER|PEM|P12`, `-pkeyopt` `rsa_padding_mode`, `rsa_oaep_md`, `rsa_mgf1_md`, `digest:` and the DigestInfo note; ML-KEM-768 key generation example in the EVP_PKEY-ML-KEM page; ML-KEM added in 3.5.0 (CHANGES.md). Removed: the engine keyform, HSM/KMS and pkcs11 claims, the Ed25519/ML-DSA rawin claim, and the grep check.
Method: documentation only; no commands were run.
