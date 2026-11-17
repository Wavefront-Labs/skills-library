---
id: mathematics.cryptographic-theory.cryptanalysis.differential-and-linear-cryptanalysis
name: differential-and-linear-cryptanalysis
category: mathematics
field: cryptographic-theory
product: cryptanalysis
tags: [cryptanalysis, differential-cryptanalysis, linear-cryptanalysis, sbox, s-box, ddt, difference-distribution-table, lat, linear-approximation-table, piling-up-lemma, characteristic, differential-trail, bias, key-recovery, last-round-attack, toy-cipher, heys-spn, spn, feistel, des, wide-trail, branch-number, frequency-analysis, vigenere, kasiski, index-of-coincidence, cryptographic-theory]
level: advanced
status: gated
description: "Attack a toy SPN with differential and linear cryptanalysis: build the DDT and LAT, chain trails with the piling-up lemma, estimate data needs and recover last-round key bits."
sources: ["Heys, A Tutorial on Linear and Differential Cryptanalysis (2002)", "Biham & Shamir, Differential Cryptanalysis of DES-like Cryptosystems (1991)", "Matsui, Linear Cryptanalysis Method for DES Cipher (1993)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Differential and linear cryptanalysis

**Goal:** carry out the two foundational statistical attacks on a small
substitution-permutation network (SPN), and use the same tables to judge a design.
Practise on a toy cipher (Heys' 16-bit, 4-round SPN is the standard exercise) (gated: unconfirmed, source is paywalled or blocked: the tutorial host did not respond).

## 0. Warm-up: classical ciphers
Same mindset, smaller scale. Substitution: frequency analysis. Vigenère: find the key
length with Kasiski repeats or the **index of coincidence** (English ≈ 0.066, random ≈
0.038), then solve each column as a Caesar shift by chi-squared against English frequencies.

## 1. S-box tables
For a 4-bit S-box S:
- **DDT** (difference distribution table): entry `[Δx][Δy] = #{x : S(x) ⊕ S(x ⊕ Δx) = Δy}`.
  Probability = entry/16. All entries are even; row 0 is [16,0,…]. Max entry (other than
  row 0) = **differential uniformity**; lower is better (4 is the best known for 4-bit bijective
  S-boxes; the PRESENT S-box has 4, checked by script).
- **LAT** (linear approximation table): entry `[a][b] = #{x : a·x = b·S(x)} − 8`.
  Bias ε = entry/16. Largest |ε| measures linearity; 1/4 is typical for good 4-bit S-boxes.
Compute both with a 10-line script; hand tables are error-prone.

## 2. Differential cryptanalysis
1. Choose an input difference ΔP and follow it through rounds: in each round, active
   S-boxes use a high-probability DDT entry; the permutation layer moves bits.
2. Trail probability ≈ product of active S-box probabilities over r−1 rounds
   (assumes independent round keys — the Markov-cipher assumption).
3. Data: about `c / p` chosen-plaintext pairs, c a small constant (≈ 5–10 in practice).
4. **Key recovery:** for each guess of the last-round key bits touching active S-boxes,
   partially decrypt each ciphertext pair one round and count how often the expected
   difference appears. The right key stands out by ~p·N; wrong keys look random.
5. Filter pairs whose ciphertext difference is zero in inactive S-boxes — removes
   most wrong pairs cheaply.

## 3. Linear cryptanalysis
1. Find a linear approximation `a·P ⊕ b·U_r = 0` (U_r = input to last round) holding with
   probability ½ + ε, by chaining LAT entries.
2. **Piling-up lemma:** for n independent approximations with biases ε_i,
   combined bias `ε = 2^{n−1} Π ε_i`.
3. Data: about `c / ε²` known plaintexts (known, not chosen — a big practical advantage).
4. Key recovery: for each last-round subkey guess, partially decrypt and count how
   often the approximation holds; the right key gives a count furthest from N/2
   (either direction — sign depends on key bits).

## 4. Using it defensively
- Count the **minimum number of active S-boxes** over r rounds (wide-trail strategy,
  branch number of the linear layer). AES guarantees ≥ 25 over 4 rounds (gated: unconfirmed, source is paywalled or blocked: Daemen and Rijmen, The Design of Rijndael), giving trail
  probability ≤ 2^{−150} (25 x 2^-6, since the AES S-box maximum DDT probability is 4/256; arithmetic checked).
- Clustering (many trails, same input/output difference) and linear hulls can make the
  real probability higher than the single best trail — trail bounds are a guide, not a proof.

## 5. Beyond
Lattice attacks on number-theoretic schemes (biased nonces, small exponents via
Coppersmith/LLL) and algebraic attacks are separate toolkits; the statistical method here
is for symmetric primitives.

## Uncertainty notes
Data-complexity constants are heuristic. Checked by script on the PRESENT S-box: DDT rows sum to 16 with all entries even and row 0 = [16,0,...]; LAT entries lie in [-8, 8] with [0][0] = 8 and maximum |entry| 4 (bias 1/4); the piling-up lemma gives bias 2^(n-1) x product (0.125 for two biases of 0.25); the English index of coincidence from standard letter frequencies is 0.0655 and uniform random is 1/26 = 0.0385. Only attack ciphers you own, toy designs, or
those in sanctioned challenges/research.

## Verify
- [ ] DDT rows sum to 16 and all entries are even; LAT entries are in [−8, 8].
- [ ] Trail probability / bias computed with independence assumptions stated.
- [ ] Data estimate (`c/p` or `c/ε²`) matches the number of pairs/texts used.
- [ ] Recovered subkey bits confirmed by decrypting fresh plaintexts.
- [ ] For a design, minimum active S-boxes per round count recorded.
