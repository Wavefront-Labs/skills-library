---
id: mathematics.cryptographic-theory.cryptographic-protocol-theory.secret-sharing-commitments-and-sigma-protocols
name: secret-sharing-commitments-and-sigma-protocols
category: mathematics
field: cryptographic-theory
product: cryptographic-protocol-theory
tags: [cryptographic-protocol-theory, secret-sharing, shamir-secret-sharing, threshold-scheme, lagrange-interpolation, verifiable-secret-sharing, feldman-vss, commitment-scheme, pedersen-commitment, hiding, binding, zero-knowledge, zero-knowledge-proof, zkp, sigma-protocol, schnorr-identification, special-soundness, honest-verifier-zero-knowledge, simulator, extractor, fiat-shamir, mpc, secure-multi-party-computation, cryptographic-theory]
level: advanced
status: verified
description: "Build and analyse the core protocol primitives: Shamir t-of-n secret sharing, Pedersen commitments, and Sigma protocols with completeness, special soundness and HVZK proofs."
sources: ["Shamir (1979), How to share a secret, CACM", "Pedersen (1991), Non-interactive and information-theoretic secure verifiable secret sharing", "Damgård, On Sigma-protocols (lecture notes)", "Boneh & Shoup, A Graduate Course in Applied Cryptography"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret sharing, commitments and Sigma protocols

**Goal:** construct these three building blocks correctly and prove the property each
one is supposed to have — they underpin threshold signatures, MPC and ZK systems.

## 1. Shamir t-of-n secret sharing
Over a prime field F_p (p > n and > secret):
1. Pick random polynomial `f(x) = s + a_1 x + … + a_{t−1} x^{t−1}` (degree t−1, f(0) = s).
2. Share i = `(i, f(i))` for i = 1 … n. **Never** use x = 0.
3. Reconstruct from any t shares by Lagrange interpolation at 0:
   `s = Σ_j y_j · Π_{m≠j} x_m / (x_m − x_j) mod p`.
- **Perfect secrecy:** any t−1 shares are consistent with every possible s
  (information-theoretic, not computational).
- **Linear:** shares of s and s' add to shares of s + s' — the basis of MPC on secrets.
- Gotchas: computing over the integers or reals instead of F_p leaks information; reusing
  the same polynomial for two secrets; no protection against a dealer or holder lying —
  that needs **verifiable** secret sharing (Feldman: publish `g^{a_k}`, each holder checks
  `g^{f(i)} = Π_k (g^{a_k})^{i^k}`; this reveals g^s, so secrecy becomes computational).

Toy check (p = 97, t = 2): f(x) = 42 + 5x → shares (1,47), (2,52); interpolation gives
`s = 47·2 − 52·1 = 42`.

## 2. Commitments
Commit(m; r) → c, later open (m, r). Two properties:
- **Hiding:** c reveals nothing about m. **Binding:** cannot open c to m' ≠ m.
- You cannot have both information-theoretically. Pick which one is perfect.
- **Pedersen:** `c = g^m h^r` in a prime-order group with `log_g h` unknown to everyone.
  Perfectly hiding; computationally binding under DLP. Additively homomorphic.
  Gotcha: if the committer knows `log_g h`, binding is gone — generate h by hashing to
  the group or by a trusted/verifiable setup.
- Hash commitments `H(m‖r)` are binding (collision resistance) and hiding in the ROM;
  r must be long and random, or low-entropy m is brute-forced.

## 3. Sigma protocols (3-move proofs of knowledge)
Template, using **Schnorr** (prove knowledge of x with y = g^x):
1. Prover: random k, send `a = g^k` (commitment).
2. Verifier: random challenge `e ∈ Z_q`.
3. Prover: `z = k + e·x mod q`. Verifier checks `g^z = a · y^e`.
Prove three properties:
- **Completeness:** honest run always verifies (substitute).
- **Special soundness:** two accepting transcripts (a, e, z), (a, e', z') with e ≠ e' give
  an **extractor**: `x = (z − z')/(e − e') mod q`. So a cheating prover succeeds with
  probability ≤ 1/q.
- **Honest-verifier zero knowledge (HVZK):** a **simulator** picks e, z at random and sets
  `a = g^z y^{−e}`; the transcript distribution equals a real one. Full ZK against
  malicious verifiers needs more (e.g. commit to the challenge first).
- **Fiat-Shamir:** replace e with `H(a ‖ y ‖ context)`. Leaving y or context out of the
  hash ("weak Fiat-Shamir") has broken deployed systems. Security argued in the ROM.
- Compose with AND (run both) and OR (Cramer-Damgård-Schoenmakers: simulate one branch,
  split the challenge) to prove compound statements.

## 4. Analysing a protocol
State the adversary model (semi-honest vs malicious, static vs adaptive corruption,
threshold t), the ideal functionality it should emulate, and prove it with a simulator
(real/ideal paradigm). Most informal "it's secure" arguments skip the malicious case.

## Uncertainty notes
Definitions follow standard texts; precise formalisms (UC vs standalone) differ and matter
for composition. The toy Shamir numbers (shares 47, 52, secret 42 mod 97), Schnorr completeness, the extractor and the HVZK simulator were run in a small group. Weak Fiat-Shamir breaking Helios is in Bernhard, Pereira and Warinschi, ASIACRYPT 2012 (DOI 10.1007/978-3-642-34961-4_38). The toy numbers are illustrative; real fields are ≥ 256 bits.

## Verify
- [ ] Shamir arithmetic is in F_p, x-coordinates non-zero and distinct, polynomial fresh per secret.
- [ ] Any t shares reconstruct; t−1 provably reveal nothing.
- [ ] For each commitment you name which property is perfect and which assumption gives the other.
- [ ] Sigma protocol has written completeness, extractor and simulator.
- [ ] Fiat-Shamir hash includes the statement and full context.
