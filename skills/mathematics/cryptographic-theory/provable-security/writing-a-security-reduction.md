---
id: mathematics.cryptographic-theory.provable-security.writing-a-security-reduction
name: writing-a-security-reduction
category: mathematics
field: cryptographic-theory
product: provable-security
tags: [provable-security, security-proof, reduction, reductionist-security, security-game, ind-cpa, ind-cca, ind-cca2, euf-cma, advantage, negligible-function, ppt-adversary, hybrid-argument, game-hopping, difference-lemma, random-oracle-model, rom, standard-model, programming-the-oracle, forking-lemma, concrete-security, tightness, hardness-assumption, cryptographic-theory]
level: advanced
status: draft
description: "Structure a cryptographic security proof: fix the game and advantage, build the reduction or a sequence of game hops, bound each step, and state tightness and the model used."
sources: ["Katz & Lindell, Introduction to Modern Cryptography (CRC)", "Shoup, Sequences of games: a tool for taming complexity in security proofs (2004)", "Bellare & Rogaway, The security of triple encryption and a framework for code-based game-playing proofs (2006)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a security reduction

**Goal:** turn "scheme Π is secure if problem P is hard" into a proof a referee can
check line by line, with an explicit bound.

## 1. Fix the definitions before anything else
Write down, as pseudocode games:
- **The security notion.** E.g. IND-CPA: challenger picks key k and bit b; adversary A
  gets an encryption oracle, submits (m0, m1) of equal length, gets Enc_k(m_b), outputs b'.
  `Adv(A) = |Pr[b' = b] − 1/2|` (or `|Pr[b'=1 | b=1] − Pr[b'=1 | b=0]|` — be consistent;
  they differ by a factor of 2).
- **The assumption**, as its own game (DDH, PRF security, factoring, LWE …) with its own advantage.
- **Resources:** running time t, number of queries q_e, q_H, etc.
Asymptotic statements say "negligible for all PPT A"; **concrete** statements say
`Adv_Π(A) ≤ c·Adv_P(B) + q²/2^n` with B's time ≈ A's time + overhead. Prefer concrete.

## 2. The reduction pattern
To prove Π secure under P, show: any A breaking Π yields B breaking P.
1. B receives a P-challenge.
2. B **simulates** A's whole environment (keys, oracles, challenge) using that instance —
   without knowing the secret.
3. B converts A's output into an answer to P.
4. Argue (a) the simulation is perfect or close, (b) B succeeds whenever A does (up to
   stated loss), (c) B's running time.
Most broken proofs fail at (a): an oracle B cannot actually answer, or a simulated
distribution that differs from the real one in a corner case.

## 3. Game hopping (when one reduction is too much)
Define Game 0 = real game, …, Game k = a game where A's advantage is 0 (e.g. the
challenge is independent of b). For each hop:
- **Indistinguishability hop:** bound `|Pr[S_i] − Pr[S_{i+1}]|` by a reduction to an assumption.
- **Failure-event hop:** games identical unless event F; **difference lemma**
  `|Pr[S_i] − Pr[S_{i+1}]| ≤ Pr[F]`; then bound Pr[F] (often a birthday term).
- **Bridging hop:** a rewrite with identical distribution; costs 0.
Sum the hops. A **hybrid argument** over q queries costs a factor q — say so.

## 4. Random-oracle model (ROM)
Hash H is modelled as a truly random function the reduction controls:
- **Observe** A's queries (extractability), **program** outputs (e.g. embed a challenge),
  keep answers consistent via a lookup table.
- Typical loss: guess which of q_H queries matters → factor q_H.
- Signatures via Fiat-Shamir use the **forking lemma** (rewind A with a different oracle
  answer); loss is roughly quadratic — Adv_P ≳ Adv²/q_H.
- ROM proofs are heuristic: there exist (contrived) schemes secure in the ROM but insecure
  with any real hash (Canetti-Goldreich-Halevi). State the model explicitly.

## 5. Tightness
A reduction with loss L means P must be L times harder than the target security level.
If `Adv_Π ≤ q_H · q_s · Adv_P`, with 2^60 queries you lose 60+ bits. Report it; it affects
parameter choice. Tight alternatives often exist at some cost.

## 6. Self-review checklist for a draft proof
- Can B answer *every* oracle query, including after the challenge, and excluding only
  what the game forbids (e.g. decrypting the challenge in IND-CCA2)?
- Are equal-length message requirements and abort probabilities accounted for?
- Is B's running time polynomial / stated?
- Is every hop's probability bound justified, with no double counting?

## Uncertainty notes
Conventions (advantage normalisation, exact forking-lemma bound) vary between texts;
match your venue's reference text. This skill describes method; it cannot check a
specific proof for you — an independent reader can.

## Verify
- [ ] Target game and assumption game are written as explicit pseudocode.
- [ ] Final theorem gives a concrete bound with time/query parameters.
- [ ] Every simulated oracle is shown to be answerable and correctly distributed.
- [ ] Each game hop is labelled (indistinguishability / failure event / bridging) with its bound.
- [ ] Model (standard vs ROM) and tightness loss are stated in the theorem.
