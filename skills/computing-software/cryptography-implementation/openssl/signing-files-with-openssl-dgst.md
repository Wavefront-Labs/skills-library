---
id: computing-software.cryptography-implementation.openssl.signing-files-with-openssl-dgst
name: signing-files-with-openssl-dgst
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, openssl-dgst, file-signing, detached-signature, ecdsa, ed25519, rsa-pss, release-signing, openssl-3]
level: practitioner
status: verified
description: "Sign and verify files with openssl dgst / pkeyutl -rawin: RSA-PSS, ECDSA and Ed25519 commands, signature formats, and why Ed25519 needs pkeyutl not dgst on older versions."
sources: ["https://docs.openssl.org/3.0/man1/openssl-dgst/", "https://docs.openssl.org/3.0/man1/openssl-pkeyutl/", "https://docs.openssl.org/3.0/man7/EVP_SIGNATURE-ED25519/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing files with openssl dgst

Detached signatures over release artifacts, config bundles or exports.

## RSA-PSS and ECDSA

```bash
# ECDSA P-256 with SHA-256 (DER-encoded signature, 70-72 bytes)
openssl dgst -sha256 -sign ec.key -out app.tar.gz.sig app.tar.gz
openssl dgst -sha256 -verify ec.pub -signature app.tar.gz.sig app.tar.gz   # "Verified OK"

# RSA-PSS (prefer over PKCS#1 v1.5 for new formats)
openssl dgst -sha256 -sign rsa.key -sigopt rsa_padding_mode:pss \
  -sigopt rsa_pss_saltlen:digest -out f.sig f
openssl dgst -sha256 -verify rsa.pub -sigopt rsa_padding_mode:pss \
  -sigopt rsa_pss_saltlen:digest -signature f.sig f
```

Extract the public key for distribution: `openssl pkey -in ec.key -pubout -out ec.pub`.

## Ed25519

Ed25519 is "pure": it hashes the message internally, so no `-sha256`.

```bash
openssl pkeyutl -sign -inkey ed.key -rawin -in f -out f.sig        # 64-byte signature
openssl pkeyutl -verify -pubin -inkey ed.pub -rawin -in f -sigfile f.sig
```

Use the pkeyutl form: `openssl dgst -sign ed.key -out f.sig f` failed on OpenSSL 3.2.3 with `Key type not supported for
this operation`. Later releases changed this (the OpenSSL 3.4/3.5 changelog implies `-rawin` for Ed25519/Ed448 with
`pkeyutl`); check your version. `-rawin` reads the whole
file into memory - fine for artifacts up to hundreds of MB, not for huge
images (sign a SHA-512 manifest instead).

## Gotchas

- `openssl dgst -sign` without a digest flag verified with `-sha256` on 3.2.3 (default SHA-256), but older versions
  defaulted differently; always pass `-sha256`.
- `-hex` output is for display; verify needs the binary signature.
- ECDSA signatures are DER `SEQUENCE{r,s}`; other tools (JWS, Web Crypto)
  expect raw `r||s` - convert, do not assume.
- "Verification failure" with no detail: run `openssl dgst ... -verify` with
  the exact digest and padding options used to sign; mismatched PSS salt is
  the usual cause.
- Signing proves who signed only if the verifier gets the public key through a
  trusted channel (pinned in the installer, published via HTTPS and a second
  channel). Consider Sigstore/cosign or minisign for release workflows with
  transparency logs.

Tested on 3.2.3: ECDSA P-256 signature was 72 bytes; Ed25519 signature 64 bytes; one-byte change gave
`Verification failure` and exit code 1.

## Verify

- [ ] Verification command prints `Verified OK` and returns exit code 0.
- [ ] Modified file (one byte) gives `Verification failure` and exit code 1.
- [ ] Public key fingerprint published out of band (`openssl pkey -pubin -in ec.pub -outform DER | sha256sum`).
