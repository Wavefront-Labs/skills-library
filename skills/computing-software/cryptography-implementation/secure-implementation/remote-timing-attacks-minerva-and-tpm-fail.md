---
id: computing-software.cryptography-implementation.secure-implementation.remote-timing-attacks-minerva-and-tpm-fail
name: remote-timing-attacks-minerva-and-tpm-fail
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, minerva-attack, tpm-fail, timing-attack, ecdsa, lattice-attack, constant-time]
level: sme
status: draft
description: "Defend against remote and local timing attacks on ECDSA like Minerva and TPM-Fail: nonce bit-length leaks, lattice recovery, constant-time scalar multiplication and testing."
sources: ["https://minerva.crocs.fi.muni.cz/", "https://tpm.fail/", "https://eprint.iacr.org/2020/728"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote timing attacks (Minerva, TPM-Fail)

## What happened
- **Minerva (2019)**: several libraries and smartcards (libgcrypt, wolfSSL, MatrixSSL, Crypto++, SunEC, Athena
  IDProtect) computed ECDSA scalar multiplication in time depending on the nonce bit length. Thousands of
  signatures with timing let a lattice attack recover the private key.
- **TPM-Fail (2019)**: Intel fTPM and STMicro TPM ECDSA/ECSchnorr signing leaked nonce length remotely; VPN server
  keys recovered over the network.
- **LadderLeak**, **Raccoon**, **Hertzbleed** extended the theme to tiny leaks, DH, and frequency scaling.

## Defences
- Constant-time scalar multiplication: fixed-length ladders or fixed-window methods that process the full scalar
  width (add `n` or `2n` to fix bit length), constant-time table access.
- Deterministic or hedged nonces do not fix timing leaks; leakage of a few bits per signature is enough.
- Update libraries and TPM firmware; prefer validated, constant-time implementations (BoringSSL, AWS-LC, formally
  verified fiat-crypto field arithmetic).
- Rate-limit and monitor signing oracles exposed to untrusted parties.

## Testing
- Collect timings for many signatures and correlate with the nonce bit length (available in test builds).
- dudect or statistical tests on signing with fixed vs random keys; Minerva authors published test tools.

## Verify
- [ ] Library versions post-date Minerva fixes; timing vs nonce-length correlation test shows no signal.
