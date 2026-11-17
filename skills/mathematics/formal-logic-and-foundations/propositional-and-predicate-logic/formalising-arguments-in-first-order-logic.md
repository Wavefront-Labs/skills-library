---
id: mathematics.formal-logic-and-foundations.propositional-and-predicate-logic.formalising-arguments-in-first-order-logic
name: formalising-arguments-in-first-order-logic
category: mathematics
field: formal-logic-and-foundations
product: propositional-and-predicate-logic
tags: [propositional-and-predicate-logic, first-order-logic, predicate-logic, propositional-logic, formalisation, translation, quantifiers, quantifier-scope, universal-quantifier, existential-quantifier, natural-deduction, truth-tables, validity, counterexample, countermodel, material-conditional, negation-of-quantifiers, prenex-normal-form, soundness, completeness, symbolic-logic]
level: practitioner
status: verified
description: "Translate an informal argument into first-order logic, then show it valid with natural deduction or invalid with a countermodel: quantifier scope, conditionals, negation and the common traps."
sources: ["Barwise & Etchemendy, Language, Proof and Logic (2nd ed., CSLI 2011)", "Enderton, A Mathematical Introduction to Logic (2nd ed., 2001)", "Magnus & Button et al., forall x: Calgary (open textbook)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Formalising arguments in first-order logic

**Goal:** take a statement or argument in words, write it precisely in first-order
logic (FOL), and settle it: a derivation if it is valid, a concrete countermodel if not.

## 1. Fix the vocabulary first
Write a *symbolisation key* before any formula:
- **Domain:** what the variables range over (people, natural numbers, everything).
  Many disputes about a formalisation are really disputes about the domain.
- **Predicates** with arity and meaning: `S(x)`: x is a student; `L(x, y)`: x likes y.
- **Constants and functions:** `a`: Alice; `f(x)`: the mother of x (functions must be
  total on the domain — "the mother of" fails for some domains).

## 2. Translation patterns (memorise these)
| English | FOL |
|---|---|
| All S are P | ∀x (S(x) → P(x)) |
| Some S are P | ∃x (S(x) ∧ P(x)) |
| No S are P | ∀x (S(x) → ¬P(x)) ≡ ¬∃x (S(x) ∧ P(x)) |
| Only S are P | ∀x (P(x) → S(x)) |
| Not all S are P | ¬∀x (S(x) → P(x)) ≡ ∃x (S(x) ∧ ¬P(x)) |
| Exactly one P | ∃x (P(x) ∧ ∀y (P(y) → y = x)) |
| A unless B | A ∨ B (equivalently ¬B → A) |
| A only if B | A → B |
| A if B | B → A |

**Two classic bugs:** `∀x (S(x) ∧ P(x))` says *everything* is an S that is P;
`∃x (S(x) → P(x))` is true as soon as anything is not an S. Universal goes with `→`,
existential with `∧`.

## 3. Quantifier order and scope
`∀x ∃y L(x, y)` (everyone likes someone) ≠ `∃y ∀x L(x, y)` (someone is liked by
everyone). The second implies the first, not conversely. When English is ambiguous
("everyone loves someone"), write both readings and say which you intend.
Mathematics example: continuity (∀ε ∃δ, δ may depend on the point) vs uniform continuity
(∃δ before ∀x).

**Negation pushes through, flipping quantifiers:** ¬∀x φ ≡ ∃x ¬φ; ¬∃x φ ≡ ∀x ¬φ;
¬(A → B) ≡ A ∧ ¬B. Negating an ε–δ definition mechanically this way is the reliable
route to "what it means to fail".

## 4. Deciding validity
An argument is **valid** iff every interpretation making the premises true makes the
conclusion true.
- **Propositional** fragments: truth table (2ⁿ rows) or, faster, try to build a
  falsifying row — assume the conclusion false and the premises true and propagate.
- **Prove valid:** natural deduction. Core moves: →I (assume A, derive B, discharge),
  ∀I (derive φ(c) for an arbitrary c not in any open assumption), ∃E (introduce a fresh
  name for the witness; it must not appear in the conclusion), ¬I / reductio.
- **Prove invalid:** give a **countermodel** — a small domain (often 1–3 elements) and
  extensions for each predicate where all premises are true and the conclusion false.
  Check each formula against it explicitly.
Soundness and completeness guarantee these two activities are exhaustive: an argument
has a derivation iff it is valid. But FOL validity is only semi-decidable — you may
search forever for either, so try small countermodels early.

## 5. Tools
Truth-table and proof checkers (e.g. the forall x / Carnap online checkers, Fitch in
LPL) catch rule misapplications. Automated provers (Prover9/Mace4, Vampire, Z3 for
decidable fragments) can find proofs or finite countermodels: Mace4 is specifically a
countermodel finder. Treat tool output as a candidate and re-check it by hand.

## Gotchas
- The material conditional is true whenever the antecedent is false; "if" in English
  often carries causal or counterfactual content FOL does not capture. Say so.
- Empty domains are excluded in standard FOL, so ∀x P(x) ⊨ ∃x P(x). Aristotelian
  "All S are P ⇒ Some S are P" fails if there are no S.
- Identity needs its own predicate `=`; "the" (definite descriptions) needs the
  uniqueness clause.
- Uncertain: conventions for ∃E/∀I side conditions differ between textbooks; follow the
  system your course or checker uses.

## Checked
Brute-forced over every interpretation on domains of 1-3 elements (Python), and with Z3 5.3.1, on 2026-10-19: no-S-are-P and not-all-S-are-P equivalences hold; ∀x P(x) ⊨ ∃x P(x) on non-empty domains; ∃y∀x L(x,y) implies ∀x∃y L(x,y) but not conversely (countermodel on 3 elements); "All S are P" with no S is satisfiable (so Aristotelian subalternation fails); `Or(A,B)` is equivalent to `Implies(Not(B),A)`; Z3 returns a model for the premises of the subalternation argument with a false conclusion. Prover9/Mace4, Carnap, forall x and Vampire pages open.

## Verify
- [ ] Symbolisation key written: domain, predicates with arity, constants.
- [ ] Each ∀ paired with →, each ∃ with ∧ (or deliberately otherwise).
- [ ] Quantifier order checked against the intended reading.
- [ ] Valid: a complete derivation (ideally machine-checked). Invalid: an explicit
      countermodel with every premise and the conclusion evaluated.
