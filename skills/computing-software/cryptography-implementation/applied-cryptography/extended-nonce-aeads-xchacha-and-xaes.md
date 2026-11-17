---
id: computing-software.cryptography-implementation.applied-cryptography.extended-nonce-aeads-xchacha-and-xaes
name: extended-nonce-aeads-xchacha-and-xaes
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, extended-nonce, xchacha20-poly1305, xaes-256-gcm, hchacha20, random-nonce, aead]
level: advanced
status: docs-checked
description: "Use extended-nonce AEADs safely: XChaCha20-Poly1305 via HChaCha20 subkeys and XAES-256-GCM, so random 192-bit nonces can be used for a very large number of messages."
sources: ["https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-xchacha", "https://c2sp.org/XAES-256-GCM"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extended-nonce AEADs

Standard 96-bit AEAD nonces are awkward to generate at random for many messages under one key. Extended-nonce
constructions derive a per-nonce subkey from part of a 192-bit nonce, so a random nonce is safe for a virtually
unlimited number of messages.

## XChaCha20-Poly1305 (draft-irtf-cfrg-xchacha, an Internet-Draft dated January 2020, not an RFC)
- Pass the key and the first 16 bytes of the 24-byte nonce to HChaCha20 to get a subkey; then use the subkey with
  ChaCha20-Poly1305 and a 12-byte nonce made of 4 zero bytes followed by the remaining 8 nonce bytes.
- In the AEAD mode the initial block counter is 1, since the first block derives the one-time Poly1305 key.
- Because it is an expired draft, check the current status of the specification before standardising on it. The
  draft includes a test vector for the HChaCha20 block function.

## XAES-256-GCM (C2SP)
- 256-bit key, 192-bit nonce, plaintext up to about 64 GiB. Derives a per-nonce AES-256 key with the NIST
  SP 800-108r1 counter-mode KDF using AES-CMAC (label `X`, first 96 bits of the nonce as context, 16-bit counter, no L
  field), then runs AES-256-GCM with the last 96 bits of the nonce.
- The C2SP page states random nonces are fine for 2^80 messages with collision risk 2^-32, that it is neither nonce
  misuse-resistant nor key-committing, and that it can be built on any library exposing AES-256-GCM plus AES-CMAC,
  AES-CBC or raw AES-256. It specifies test vectors.

## Guidance
- Pick extended-nonce when nonces are random and key lifetime or message count is open-ended (stored data, many
  writers sharing a key).
- Never reuse a nonce on purpose; neither construction resists nonce misuse.
- Store the full 24-byte (192-bit) nonce with each ciphertext.

## Verify
- [ ] Test vectors from the C2SP page (XAES) or the draft's HChaCha20 vector (XChaCha) pass.
- [ ] Nonce comes from a CSPRNG, 24 bytes, per message.

## Checked
2026-11-01. Confirmed against the C2SP XAES-256-GCM specification (v1.0.1) and draft-irtf-cfrg-xchacha sections
2.2 to 2.3. Removed: the random-IV GCM invocation limit attributed to NIST, the FIPS status of XChaCha20-Poly1305,
and the list of libraries and function names (none are in the cited specifications).
Method: documentation only; no commands were run.
