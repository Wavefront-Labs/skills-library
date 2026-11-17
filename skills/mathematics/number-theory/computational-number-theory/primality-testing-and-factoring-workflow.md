---
id: mathematics.number-theory.computational-number-theory.primality-testing-and-factoring-workflow
name: primality-testing-and-factoring-workflow
category: mathematics
field: number-theory
product: computational-number-theory
tags: [computational-number-theory, primality-testing, miller-rabin, baillie-psw, bpsw, ecpp, primality-certificate, aks, probable-prime, carmichael-numbers, integer-factorisation, integer-factorization, trial-division, pollard-rho, pollard-p-minus-1, ecm, elliptic-curve-method, quadratic-sieve, gnfs, msieve, cado-nfs, yafu, gmp-ecm, pari-gp, sympy]
level: practitioner
status: gated
description: "Decide whether a large integer is prime and factor it efficiently: Miller–Rabin and BPSW, certificates (ECPP), then a staged pipeline of trial division, rho, p−1, ECM, and QS/NFS by size."
sources: ["Crandall & Pomerance, Prime Numbers: A Computational Perspective (2nd ed., Springer 2005)", "Cohen, A Course in Computational Algebraic Number Theory (Springer GTM 138)", "Pomerance, Selfridge & Wagstaff, The pseudoprimes to 25·10^9 (Math. Comp. 1980)", "PARI/GP, GMP-ECM and CADO-NFS documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Primality testing and factoring workflow

**Goal:** for an integer N (up to hundreds of digits), decide primality with the right
level of certainty and, if composite, find its factorisation with the cheapest method
that will finish.

## 1. Primality: three levels of certainty
1. **Probable prime (fast).** Miller–Rabin with random bases: a composite passes one round
   with probability ≤ 1/4 (far less in practice). **Baillie–PSW** (a base-2 strong test
   plus a strong Lucas test) has no known counterexample and is what PARI's
   `ispseudoprime`, SymPy's `isprime` (its docstring cites Baillie-Wagstaff, "Lucas Pseudoprimes"), GMP's `mpz_probab_prime_p` (gated: unconfirmed, source is paywalled or blocked) and most libraries use.
2. **Deterministic for bounded N.** Fixed Miller–Rabin base sets are proven correct below
   explicit bounds — e.g. bases {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37} suffice
   for all N < 3.18·10²³ (Sorenson–Webster; adding 41 extends this to ~3.3·10²⁴) (gated: unconfirmed, source is paywalled or blocked). Use published sets only, cited.
3. **Proven prime (certificate).** ECPP (PARI `primecert(N)` returns a checkable certificate and `primecertisvalid(cert)` checks it (both in the PARI manual); Primo for thousands of digits) or N−1/N+1 methods when those
   numbers factor well (Pocklington/BLS). AKS is polynomial-time but slow in practice —
   theoretical interest only.
Plain Fermat tests (a^{N−1} ≡ 1) are fooled by **Carmichael numbers** (computed: 561, 1105, 1729, 2465, 2821 pass every coprime Fermat base tried);
don't use them alone.

## 2. Factoring pipeline (stop as soon as the cofactor is prime)
Always run a primality test on each cofactor between stages.
| Stage | Finds factors up to roughly | Tool |
|---|---|---|
| trial division | 10⁶–10⁸ | any; also catches small primes cheaply |
| Pollard rho (Brent) | ~10¹²–10¹⁵ (≈ 15 digits) (gated: unconfirmed, source is paywalled or blocked) | PARI `factor`, SymPy `pollard_rho` |
| Pollard p−1 / Williams p+1 | any p with p−1 (p+1) smooth | GMP-ECM `-pm1`, `-pp1` |
| ECM | ~20–60 digits (record ~80) (gated: unconfirmed, source is paywalled or blocked) | GMP-ECM, PARI `factor` (internally), YAFU |
| quadratic sieve (SIQS) | N up to ~100 digits (gated: unconfirmed, source is paywalled or blocked) | YAFU, msieve |
| number field sieve (GNFS) | N above ~100 digits | CADO-NFS, msieve+GGNFS |
ECM's run time depends on the size of the **factor**, QS/NFS on the size of **N**: run
ECM to a sensible depth (e.g. curves at B1 = 11e3, 5e4, 2.5e5, 1e6, 3e6 per GMP-ECM's
recommended table (gated: unconfirmed, source is paywalled or blocked)) before committing to a sieve. Integrated drivers (YAFU's `factor()`,
PARI's `factor`) choose the stages automatically and are the right default.

## 3. Special forms
Numbers of the form aⁿ ± b with small a, b: use SNFS (much faster than GNFS) and check
existing tables (Cunningham project, factordb.com) first — many have been factored
already. N = p·q with |p − q| small: Fermat's method finishes immediately. Shared
factors across many RSA-like moduli: batch gcd.

## 4. Practical commands
```
\\ PARI/GP
ispseudoprime(N)          \\ BPSW
isprime(N)                \\ proven primality (see the PARI manual for the method used)
factor(N)                 \\ full pipeline incl. rho, ECM, MPQS
factorint(N, 1)           \\ flags control methods
```
```python
import sympy
sympy.isprime(n); sympy.factorint(n)      # ran: factorint(2**67-1) = 193707721 * 761838257287; slow on hard inputs
```
`echo N | ecm -c 100 1e6` (GMP-ECM: 100 curves, B1 = 10⁶; not run here (gated: unconfirmed, source is paywalled or blocked)).

## 5. Discrete logs and related
Discrete logarithms mod p: baby-step giant-step / Pollard rho for small groups, Pohlig–
Hellman when p − 1 is smooth, index calculus/NFS-DL for large p (`znlog` in PARI).
These complexities mirror factoring; a safe prime makes Pohlig–Hellman useless.

## Gotchas
- "Probable prime" is not "prime"; for publication or cryptographic parameters produce
  a certificate.
- SymPy is convenient but orders of magnitude slower than PARI/YAFU/GMP-ECM on hard
  inputs.
- Factoring 2048-bit RSA moduli is infeasible with all public methods; don't plan on it.
- Uncertain: the size ranges in the table are rough rules of thumb that move with
  hardware and software versions; benchmark on your machine.

## Verify
- [ ] Product of reported factors equals N exactly.
- [ ] Each reported prime factor passed BPSW, and is proven when it must be.
- [ ] Composite cofactors are flagged as composite, not silently left in.
- [ ] Method choice justified by factor/N size; ECM depth recorded before sieving.
