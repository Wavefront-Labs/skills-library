---
id: computing-software.systems-network-administration.pki-tls-administration.openssl-keygen-algorithms
name: openssl-keygen-algorithms
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [openssl-keygen-algorithms, pki-openssl-csr, openssl, genpkey, ecdsa, rsa, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Generate RSA, ECDSA and Ed25519 private keys with openssl genpkey, protect them and choose sizes and curves."
sources:
  - https://docs.openssl.org/master/man1/openssl-genpkey/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSSL key generation
Goal: create a strong key with correct permissions.
```
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out leaf.key
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out rsa.key
openssl genpkey -algorithm ED25519 -out ed.key
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -aes-256-cbc -out ca.key   # passphrase-protected CA key
chmod 600 *.key
```
- `genpkey` is the algorithm-neutral generator and writes PKCS#8; `genrsa` is the RSA-only command.
- Algorithm choice is yours: P-256 or P-384 for ECDSA, RSA 3072 or more where ECDSA is not supported. Check what your CA and clients accept before using Ed25519.
- Never commit keys to Git or pass passphrases on the command line (`-pass file:path` or a prompt).
Gotcha: some tools need the traditional key format and others PKCS#8. `openssl pkey -traditional` writes the traditional format; `openssl pkcs8 -topk8 -nocrypt` writes unencrypted PKCS#8.
Verify:
- [ ] `openssl pkey -in leaf.key -noout -text` prints the key parameters you intended.
- [ ] File mode is 600 and owner is the service account.

## Checked
2026-11-03. Confirmed in the openssl-genpkey, openssl-genrsa, openssl-pkey and openssl-pkcs8 manual pages: `-algorithm` values EC, RSA and ED25519, `-pkeyopt ec_paramgen_curve` with NIST names such as `P-256`, `rsa_keygen_bits`, `-aes-256-cbc` style cipher options, `-pass`, PKCS#8 output, `pkey -traditional -noout -text`, `pkcs8 -topk8 -nocrypt`. Removed: the claim that public CAs reject Ed25519, the PKCS#1 `BEGIN RSA PRIVATE KEY` text, `ecparam`, the `head -3` pipe and the claim that P-384 suits CAs (a choice, now worded as one).
Method: documentation only; no commands were run.
