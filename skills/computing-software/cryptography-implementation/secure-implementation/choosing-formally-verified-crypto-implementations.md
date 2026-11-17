---
id: computing-software.cryptography-implementation.secure-implementation.choosing-formally-verified-crypto-implementations
name: choosing-formally-verified-crypto-implementations
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, crypto-code-review, verified-cryptography, hacl-star, fiat-crypto, aws-lc-saw, formal-verification, memory-safety]
level: sme
status: docs-checked
description: "Use formally verified crypto where it counts: what HACL*, fiat-crypto, s2n-bignum and the AWS-LC proofs claim, their status, and the gaps proofs do not cover."
sources: ["https://hacl-star.github.io/", "https://github.com/mit-plv/fiat-crypto", "https://github.com/awslabs/aws-lc-verification", "https://github.com/awslabs/s2n-bignum"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing formally verified crypto implementations

Formal verification proves properties of code against a mathematical specification. For crypto
primitives that means fewer of the classic bugs: arithmetic errors, buffer overflows,
secret-dependent behaviour.

## What is available (from the project pages)

| Project | What it claims |
|---|---|
| HACL* (F*, Low*, compiled to C by KaRaMeL) | Verified for memory safety, functional correctness and secret independence (resistance to some timing side channels). Algorithms include Curve25519, Ed25519, AES-GCM, Chacha20, Poly1305, SHA-2, SHA-3, HMAC and HKDF |
| ValeCrypt | Verified assembly for selected primitives, proved memory safe, functionally correct and secret independent in timing and memory access |
| EverCrypt | Provider combining HACL* and ValeCrypt, picks the fastest implementation for the CPU; agile API |
| fiat-crypto (Coq) | Synthesises code for finite-field arithmetic; the repository cites a thesis titled "Correct-by-Construction Finite Field Arithmetic in Coq" |
| s2n-bignum (HOL Light) | Functions for x86_64 and Arm, written in a constant-time style, with proofs in HOL Light |
| aws-lc-verification | Specifications and proofs verifying portions of AWS-LC; older proofs used SAW (C and x86_64) and NSym (AArch64) with Cryptol specs and some Coq proofs |

Deployment and status notes from those pages:

- HACL*, ValeCrypt and EverCrypt code is deployed in several production systems per the HACL*
  manual, including Mozilla Firefox's NSS, the Linux kernel, mbedTLS, Tezos, ElectionGuard and
  WireGuard. The manual also says they remain ongoing research projects and should be treated as
  such, and to talk to the maintainers before integrating into production.
- The HACL* repository states it is in maintenance mode: no new features, defect fixes accepted.
- The AWS-LC verification effort moved to s2n-bignum (HOL Light) for assembly on x86_64 and
  AArch64 and to CBMC for C components such as ML-KEM in mlkem-native; the SAW and NSym proofs
  stay in CI.

## How to use this when choosing a library

- Check per algorithm and per platform which code path is verified; the proofs cover specific
  code, not the whole library.
- Pin versions and track which algorithms the proofs cover.

## What proofs do not cover

- The specification itself (a wrong spec gives a verified wrong program).
- API misuse by the caller.
- Compiler and hardware effects: HACL* secret independence is at source level.
- Glue code, build flags and the unverified parts of the same library.
- Side channels beyond the modelled ones.

## Verify

- [ ] For each critical primitive, record which implementation and backend runs in production.
- [ ] The library version is covered by the published proofs.
- [ ] Application-level review and tests remain in place.

## Checked

Method: docs-checked 2026-11-09 against hacl-star.github.io landing page, the hacl-star repository README, mit-plv/fiat-crypto README, awslabs/aws-lc-verification README, awslabs/s2n-bignum README. Removed: the libcrux row and its sources (README not fetchable), the "ships in" claims for fiat-crypto (BoringSSL, Go, Chrome, AWS-LC), Python hashlib, Project Everest items EverParse and miTLS deployment claims, the P-256 and ML-KEM coverage lists for HACL*, and the AWS-LC algorithm list (AES-GCM, HMAC, ECDSA, ML-KEM equivalence).
