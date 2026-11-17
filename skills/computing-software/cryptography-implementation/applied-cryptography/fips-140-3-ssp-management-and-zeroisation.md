---
id: computing-software.cryptography-implementation.applied-cryptography.fips-140-3-ssp-management-and-zeroisation
name: fips-140-3-ssp-management-and-zeroisation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ssp-zeroisation, fips-140-3, sensitive-security-parameters, zeroization, csp, iso-19790]
level: sme
status: draft
description: "Meet FIPS 140-3 SSP management requirements (ISO 19790 7.9): SSP inventory, entry and output methods, storage, and zeroisation procedures that a lab will test."
sources: ["https://csrc.nist.gov/projects/cryptographic-module-validation-program/fips-140-3-standards", "https://csrc.nist.gov/csrc/media/Projects/cryptographic-module-validation-program/documents/fips%20140-3/FIPS%20140-3%20IG.pdf", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-140Br1.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FIPS 140-3 SSP management and zeroisation

SSPs = CSPs (secret/private keys, passwords, DRBG state) plus PSPs (public keys whose integrity matters).

## Security policy must document (SP 800-140B)
A table per SSP: name, type and size, strength, generation (DRBG, KDF), entry/output method (plaintext,
wrapped, split knowledge), storage location and form, zeroisation method, and which services use it.

## Requirements to design for
- **Generation**: from an approved DRBG or KDF; record the strength.
- **Entry/output**: Level 1-2 may allow plaintext over a trusted channel; Level 3+ require encrypted or split
  knowledge entry for CSPs crossing the boundary.
- **Zeroisation**: all unprotected SSPs must be zeroisable. Procedural (power off for RAM) or explicit service.
  Level 2+ need the zeroisation status indicated. Must cover copies in buffers, caches and stack.
- Temporary SSPs (intermediate key schedules, ECDH shared secrets) must be zeroised when no longer needed.

## Implementation
- Use explicit wipe functions resistant to dead-store elimination (`OPENSSL_cleanse`, `explicit_bzero`).
- Free paths: every `free` of a key struct goes through a cleanse.
- Provide a zeroise service (`zeroize` command/API) that clears persistent keys and returns status.

## Verify
- [ ] Lab-style test: dump memory after zeroise service and after normal key free; no SSP bytes remain.
