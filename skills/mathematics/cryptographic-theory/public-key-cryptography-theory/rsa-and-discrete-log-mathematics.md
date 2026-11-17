---
id: mathematics.cryptographic-theory.public-key-cryptography-theory.rsa-and-discrete-log-mathematics
name: rsa-and-discrete-log-mathematics
category: mathematics
field: cryptographic-theory
product: public-key-cryptography-theory
tags: [public-key-cryptography-theory, rsa, euler-totient, carmichael-function, modular-exponentiation, modular-inverse, extended-euclid, chinese-remainder-theorem, crt, fermat-little-theorem, discrete-logarithm, diffie-hellman, cdh, ddh, elgamal, schnorr, dsa, ecdsa, elliptic-curve, ecc, group-order, cofactor, pohlig-hellman, textbook-rsa, padding, oaep, pss, sage, cryptographic-theory, number-theory]
level: advanced
status: gated
description: "Work the number theory behind RSA and discrete-log systems by hand or in Sage: key generation, CRT, why textbook RSA fails, DH group choice, and the nonce rule for Schnorr/DSA."
sources: ["Hoffstein, Pipher & Silverman, An Introduction to Mathematical Cryptography (Springer)", "Galbraith, Mathematics of Public Key Cryptography (CUP)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RSA and discrete-log mathematics

**Goal:** be able to derive, check and break-test the core public-key schemes from the
underlying number theory, and know which "obvious" constructions are insecure.

## 1. RSA
Key generation:
1. Random primes p, q of equal size; `N = pq`.
2. `λ(N) = lcm(p−1, q−1)` (Carmichael) — or `φ(N) = (p−1)(q−1)`; both work.
3. Public exponent `e` (usually 65537) with `gcd(e, λ(N)) = 1`.
4. `d = e^{−1} mod λ(N)` by the extended Euclidean algorithm.
Correctness: `m^{ed} ≡ m (mod N)` for all m, by Fermat/Euler on each prime and CRT.

**CRT speed-up:** `d_p = d mod (p−1)`, `d_q = d mod (q−1)`, compute `m_p = c^{d_p} mod p`,
`m_q = c^{d_q} mod q`, recombine with `q_inv = q^{−1} mod p`:
`m = m_q + q·((m_p − m_q)·q_inv mod p)`. (speed-up factor gated: unconfirmed, source is paywalled or blocked).
Gotcha: a single faulty CRT half leaks a factor: `gcd(s^e − m, N)` = p or q (Bellcore attack).

Hand-check example: p=61, q=53, N=3233, φ=3120, e=17, d=2753. `65^17 mod 3233 = 2790`;
`2790^2753 mod 3233 = 65`.

### Why textbook RSA is insecure
- **Deterministic** → not IND-CPA; guess-and-check small message spaces.
- **Malleable:** `c·r^e` decrypts to `m·r` → chosen-ciphertext attacks.
- Small e with small m and no padding: `m^3 < N` → take the integer cube root.
- Same m to e recipients → Håstad broadcast via CRT.
Fix: **OAEP** for encryption, **PSS** for signatures (proofs in the random-oracle model).
Factoring N breaks RSA; whether the converse holds is open (RSA assumption is ≤ factoring).

## 2. Discrete-log systems
In a cyclic group G = ⟨g⟩ of prime order q:
- **DLP:** given g^x find x. **CDH:** given g^a, g^b find g^{ab}. **DDH:** distinguish
  g^{ab} from random. DLP ⇒ CDH ⇒ DDH in hardness ordering (breaking DLP breaks the rest).
- **Diffie-Hellman:** share g^a, g^b; key g^{ab}. Unauthenticated → man-in-the-middle.
- **ElGamal:** `(g^r, m·h^r)`, h = g^x. IND-CPA under DDH; malleable.

### Group choice — the part that goes wrong
- In `Z_p^*` the order is p−1, which has small factors; **Pohlig-Hellman** solves DLP in
  each small subgroup. Use a prime-order subgroup (safe prime p = 2q+1) and validate that
  received elements lie in it (small-subgroup / invalid-curve attacks).
- Elliptic curves: group order `#E = h·n` with cofactor h; work in the order-n subgroup;
  check points are on the curve. Generic DLP cost √n (Pollard rho), so a 256-bit curve
  ≈ 128-bit security, while `Z_p^*` needs ~3072-bit p for the same (index calculus).

## 3. Schnorr / DSA / ECDSA signatures
Schnorr: commit `R = g^k`, challenge `e = H(R‖m)`, response `s = k + x·e mod q`.
- **The nonce k must be secret, uniform and never reused.** Two signatures with the
  same k: `x = (s1 − s2)/(e1 − e2) mod q`. Even a few biased bits of k across many
  signatures leak x via lattice (hidden-number problem) attacks.
- Deterministic nonces (RFC 6979 / EdDSA) remove the RNG dependency.

## 4. Doing it in practice
Sage: `p = random_prime(2^512); Zmod(N)`, `inverse_mod(e, lcm(p-1,q-1))`,
`discrete_log(Mod(h,p), Mod(g,p))` for toy sizes; `EllipticCurve(GF(p),[a,b]).order()`.
Python: `pow(e, -1, phi)` (3.8+) and `pow(m, e, N)`.

## Uncertainty notes
Security-level equivalences: NIST SP 800-57 Part 1 Rev. 5 Table 2 lists 128-bit strength for
L = 3072 (FFC) and k = 3072 (IFC), N = 256 (confirmed). Sage function names, the Håstad,
OAEP/PSS and Bellcore attributions are (gated: unconfirmed, source is paywalled or blocked).
This is theory: production code must use a vetted library, never these formulas directly.

## Verify
- [ ] `e·d ≡ 1 (mod λ(N))` and a round-trip encrypt/decrypt works on test values.
- [ ] CRT recombination gives the same result as direct exponentiation.
- [ ] You can explain each textbook-RSA attack and which padding prevents it.
- [ ] DH/EC group has prime order (or cofactor handled) and inputs are validated.
- [ ] Signature nonces are unique and unbiased (or deterministic per RFC 6979/EdDSA).
