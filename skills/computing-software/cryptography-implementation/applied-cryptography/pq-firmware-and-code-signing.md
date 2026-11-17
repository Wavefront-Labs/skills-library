---
id: computing-software.cryptography-implementation.applied-cryptography.pq-firmware-and-code-signing
name: pq-firmware-and-code-signing
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hash-based-signatures, pq-firmware-signing, secure-boot, code-signing, lms, slh-dsa, ml-dsa, cnsa-2, post-quantum]
level: sme
status: draft
description: "Plan post-quantum firmware and code signing: why boot ROMs need PQ now, LMS vs SLH-DSA vs ML-DSA for verifiers, dual signing during transition, and size/speed checks."
sources: ["https://media.defense.gov/2022/Sep/07/2003071834/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS_.PDF", "https://csrc.nist.gov/pubs/sp/800/208/final", "https://csrc.nist.gov/pubs/fips/205/final", "https://csrc.nist.gov/pubs/ir/8547/ipd"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-quantum firmware and code signing

Devices shipped today with a signature verifier burned into ROM or OTP will
still be in the field when a cryptographically relevant quantum computer could
forge RSA/ECDSA signatures. Firmware signing is therefore the first place to
deploy PQ signatures; CNSA 2.0 asks for it to be preferred from 2025 and
exclusive by 2030.

## Pick the verifier algorithm

| Algorithm | Why | Watch out for |
|---|---|---|
| LMS/HSS (SP 800-208) | Tiny verifier code (hash only), small sigs (~1-5 KB), CNSA 2.0 named | Stateful: signing in HSM, limited signature count |
| SLH-DSA (FIPS 205) | Stateless, hash-only security | 8-50 KB signatures, slow signing |
| ML-DSA (FIPS 204) | Fast, ~2.4-4.6 KB sigs, general purpose | Larger verifier code, lattice assumptions, more RAM |

For boot ROM verifiers with a few KB of code and SHA-256 hardware, LMS is the
common choice; release signing happens rarely and in an HSM, which suits the
state requirement.

## Transition design

- **Dual signing**: sign images with both the classical key (ECDSA P-384 or
  RSA-3072) and the PQ key. Old devices verify classical; new devices require
  PQ (and optionally both). Store both signatures in the image header with
  algorithm ids.
- **Key hierarchy**: root public key hash in OTP/ROM; root signs a
  manifest of intermediate signing keys; intermediates sign images. Rotating
  intermediates does not touch silicon. Choose the root algorithm most
  carefully: it is fixed for the device lifetime.
- **Reserve space** in header formats for PQ signature and key sizes now.
- **Anti-rollback**: version counters in secure storage apply unchanged.

## Measure on target

Verify time, code size and stack/RAM for the verifier on the actual MCU;
for SLH-DSA the hash count dominates, for ML-DSA the RAM.

## Verify

- [ ] Image format carries algorithm ids and room for PQ signatures.
- [ ] ROM/bootloader verifier passes the algorithm's KAT vectors on hardware.
- [ ] Signing keys for LMS live in an HSM with state management.
- [ ] Documented date after which devices reject classical-only images.
