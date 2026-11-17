---
id: mathematics.cryptographic-theory.post-quantum-cryptography.learning-with-errors-and-lattice-hardness
name: learning-with-errors-and-lattice-hardness
category: mathematics
field: cryptographic-theory
product: post-quantum-cryptography
tags: [post-quantum-cryptography, pqc, quantum-resistant, lattice-cryptography, lwe, learning-with-errors, ring-lwe, module-lwe, sis, short-integer-solution, svp, cvp, lattice-reduction, lll, bkz, lattice-estimator, regev-encryption, kyber, ml-kem, fips-203, dilithium, ml-dsa, fips-204, sphincs, slh-dsa, fips-205, hash-based-signatures, shor, grover, isogeny, sike, cryptographic-theory]
level: advanced
status: gated
description: "Understand LWE/Module-LWE and SIS as the hardness behind ML-KEM and ML-DSA: Regev encryption by hand, why the error matters, and how parameters are sized against lattice reduction."
sources: ["Regev (2005), On lattices, learning with errors, random linear codes, and cryptography", "Peikert, A Decade of Lattice Cryptography (2016)", "NIST FIPS 203, 204, 205 (2024)", "Albrecht et al., lattice-estimator (GitHub)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Learning with errors and lattice hardness

**Goal:** reason about the post-quantum schemes now being standardised from their maths,
starting from LWE, and know what the hardness claims do and don't say.

## 1. Why "post-quantum"
Shor's algorithm solves factoring and discrete log in polynomial time on a large
fault-tolerant quantum computer → RSA, DH, ECC fall. Grover only square-roots brute force
→ symmetric keys and hashes survive with doubled sizes (AES-256). PQC replaces the
public-key layer with problems that have no known efficient quantum algorithm:
lattices, codes, hash functions, multivariate systems, isogenies.

## 2. LWE
Parameters n (dimension), modulus q, error distribution χ (small, e.g. discrete Gaussian
or centred binomial with width ~ a few units).
- Sample: secret `s ∈ Z_q^n`; public random matrix `A ∈ Z_q^{m×n}`; small error e ← χ^m;
  `b = A s + e mod q`.
- **Search-LWE:** find s from (A, b). **Decision-LWE:** distinguish (A, b) from uniform.
  Equivalent for suitable parameters.
- Without e it is Gaussian elimination — the error *is* the security. With e it reduces
  (Regev, quantumly; Peikert, classically for some parameters) to **worst-case** lattice
  problems (GapSVP, SIVP). This worst-case → average-case link is what makes lattices attractive.
- **SIS** (dual): find short non-zero z with `A z = 0 mod q`. Underlies hash-and-sign /
  Fiat-Shamir-with-aborts signatures.

## 3. Regev encryption (one bit)
- Key: public (A, b = As + e), secret s.
- Encrypt bit μ: random 0/1 vector r; `u = rᵀA`, `v = rᵀb + μ·⌊q/2⌋`.
- Decrypt: `v − u·s = rᵀe + μ⌊q/2⌋`. If `|rᵀe| < q/4`, round to the nearest of {0, q/2}.
- **Correctness condition:** accumulated error < q/4. Parameter design trades error width
  (security) against q (decryption failure, size). Real schemes accept a tiny failure
  probability (FIPS 203 Table 1: 2^-138.8 for ML-KEM-512, 2^-164.8 for ML-KEM-768, 2^-174.8 for ML-KEM-1024) — failures can leak key information,
  which is why the bound matters.

## 4. Ring/Module-LWE and the standards
Replace Z_q^n by the ring `R_q = Z_q[x]/(x^n + 1)` (n a power of 2) for compact keys and
NTT-fast multiplication. Module-LWE uses small matrices over R_q (rank k), tuning security
by k without changing the ring.
- **ML-KEM** (FIPS 203, from Kyber): Module-LWE, n = 256, q = 3329, k = 2/3/4 for the
  512/768/1024 sets. IND-CCA via a Fujisaki-Okamoto transform.
- **ML-DSA** (FIPS 204, from Dilithium): Module-LWE + Module-SIS, Fiat-Shamir with aborts.
- **SLH-DSA** (FIPS 205, from SPHINCS+): hash-based only — conservative, large signatures.
- **Isogenies:** SIKE was broken classically in 2022 (Castryck-Decru); a reminder that
  "no known attack" is a moving claim.

## 5. Sizing parameters
Security is estimated, not proved: model the best attacks (primal/dual lattice attacks
using BKZ with block size β; cost ~2^{0.292β} classical sieving, lower quantum) and pick
n, q, χ so cost exceeds the target. Use the **lattice-estimator** (Sage) rather than
hand formulas: `LWE.estimate(LWE.Parameters(n=..., q=..., Xs=..., Xe=...))`.
Structured (ring/module) variants are assumed about as hard as unstructured; this is a
belief supported by cryptanalysis, not a theorem.

## Uncertainty notes
n = 256, q = 3329, k = 2/3/4 and the failure rates were read from FIPS 203 (Tables 1 and 2). The NIST PQC project page says HQC was selected on March 11, 2025 and that Falcon (FN-DSA) standardisation is underway. The `LWE.Parameters` / `LWE.estimate` names and `from estimator import *` are in the lattice-estimator README and source (not run: needs Sage). The 2^{0.292β} sieving exponent is a commonly cited asymptotic (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] You can show decryption error `rᵀe` stays below q/4 for your toy parameters.
- [ ] You can explain why removing e makes LWE trivial.
- [ ] You can name which problem (LWE vs SIS vs hash) each standard scheme relies on.
- [ ] Parameter security came from the lattice-estimator, not a back-of-envelope.
- [ ] Hybrid (classical + PQ) deployment and decryption-failure leakage considered.
