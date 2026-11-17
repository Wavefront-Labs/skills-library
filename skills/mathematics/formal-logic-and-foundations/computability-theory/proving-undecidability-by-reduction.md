---
id: mathematics.formal-logic-and-foundations.computability-theory.proving-undecidability-by-reduction
name: proving-undecidability-by-reduction
category: mathematics
field: formal-logic-and-foundations
product: computability-theory
tags: [computability-theory, undecidability, decidability, halting-problem, many-one-reduction, turing-reduction, rices-theorem, recursively-enumerable, semi-decidable, co-re, turing-machines, diagonalisation, recursion-theorem, post-correspondence-problem, arithmetical-hierarchy, computable-functions, church-turing-thesis, mapping-reduction]
level: advanced
status: draft
description: "Show a problem is undecidable (or not even semi-decidable) by reducing the halting problem to it, apply Rice's theorem correctly, and place problems in the r.e./co-r.e. picture."
sources: ["Sipser, Introduction to the Theory of Computation (3rd ed., 2012), ch. 4-6", "Soare, Turing Computability (Springer 2016)", "Rogers, Theory of Recursive Functions and Effective Computability (1967)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Proving undecidability by reduction

**Goal:** given a decision problem P, prove it has no algorithm — usually by a
reduction from the halting problem — and say precisely how undecidable it is.

## 1. The facts you build on
- **HALT** = {⟨M, w⟩ : TM M halts on input w} is semi-decidable (r.e.: simulate and
  accept if it halts) but not decidable (diagonal argument).
- Its complement is therefore **not** r.e. (if both a set and its complement are r.e.,
  the set is decidable — run both semi-deciders in parallel).
- Church–Turing thesis lets you describe machines in pseudocode; reductions are
  ordinary programs that *build* programs.

## 2. The reduction template (many-one / mapping)
To show P undecidable: give a **computable** f with x ∈ HALT ⇔ f(x) ∈ P.
Then a decider for P would decide HALT. Direction matters: **reduce the known-hard
problem TO the new one** (HALT ≤ P), never the other way.

Worked example: EMPTY = {⟨M⟩ : L(M) = ∅}.
Given ⟨M, w⟩, construct M′: "on input x, ignore x, run M on w; if it halts, accept."
- M halts on w ⇒ L(M′) = Σ* ≠ ∅; M doesn't halt ⇒ L(M′) = ∅.
- So ⟨M, w⟩ ∈ HALT ⇔ ⟨M′⟩ ∉ EMPTY: HALT ≤ complement(EMPTY). Hence EMPTY is
  undecidable, and more: complement(EMPTY) is r.e. but EMPTY is co-r.e. and not r.e.
Note f only *writes* M′; it never runs M. That is why f is computable.

## 3. Rice's theorem (shortcut — use it carefully)
Every **non-trivial semantic** property of the language recognised by a TM is
undecidable. Before invoking it, check:
1. **Semantic:** depends only on L(M), not on M's code (states, steps, size). "M has 17
   states" is decidable — not semantic. "M halts within 100 steps on ε" is decidable —
   not about L(M).
2. **Non-trivial:** some TM has it, some doesn't.
Rice gives undecidability only; it does not tell you whether the property is r.e.,
co-r.e. or neither. (Rice–Shapiro helps there: an r.e. semantic property must be
determined by finite sub-languages.)

## 4. Classifying the degree of unsolvability
| Example | Class |
|---|---|
| HALT, "L(M) ≠ ∅", Post Correspondence, Hilbert's 10th problem (Diophantine solvability) | Σ₁ (r.e.), complete |
| "L(M) = ∅", "M never halts on w" | Π₁ (co-r.e.) |
| "L(M) is finite", TOTAL ("M halts on all inputs") | Σ₂ / Π₂ |
| "L(M) is recursive" | Σ₃ |
Read the quantifier structure: "∃ a halting computation" is Σ₁; "∀ inputs ∃ halting
computation" is Π₂. Place a problem by writing its definition with the quantifiers
over computations made explicit, then prove hardness by reduction from a complete set at
that level.

## 5. Other tools
- **Turing reductions** (P decidable with an oracle for Q) give undecidability too but
  lose the r.e. information; prefer many-one when you want the fine classification.
- **Recursion theorem:** programs can obtain their own code. Gives slick proofs (a
  machine that does the opposite of what a purported decider predicts about itself) and
  fixed-point results.
- **Reductions from PCP** are the standard route for grammar problems (ambiguity of
  CFGs, emptiness of intersection of two CFLs).

## Gotchas
- Reducing P to HALT proves nothing about P being hard (everything r.e. reduces to
  HALT).
- The constructed machine must be a fixed object computable from the input; "if M halts,
  output Y else output N" is not computable.
- Undecidable ≠ intractable: undecidable problems often have decidable restrictions
  (bounded inputs, specific grammar classes), and decidable ones can be infeasible.
- Uncertain: hierarchy placements in the table are standard results, but levels for
  less common properties should be derived, not looked up.

## Verify
- [ ] Reduction direction is (known undecidable) ≤ (new problem).
- [ ] f is clearly computable and never simulates to completion.
- [ ] Both directions of x ∈ A ⇔ f(x) ∈ B argued.
- [ ] Rice's theorem applied only to non-trivial properties of L(M).
- [ ] r.e./co-r.e. status stated, with the quantifier structure written out.
