---
id: mathematics.formal-logic-and-foundations.proof-theory.sequent-calculus-and-cut-elimination
name: sequent-calculus-and-cut-elimination
category: mathematics
field: formal-logic-and-foundations
product: proof-theory
tags: [proof-theory, sequent-calculus, gentzen, lk, lj, cut-elimination, hauptsatz, subformula-property, structural-rules, weakening, contraction, exchange, intuitionistic-logic, classical-logic, proof-search, consistency, godel-incompleteness, ordinal-analysis, natural-deduction, linear-logic]
level: advanced
status: draft
description: "Work in Gentzen's sequent calculus: read and build LK/LJ derivations, use cut elimination and the subformula property for proof search and consistency, and see where incompleteness bites."
sources: ["Troelstra & Schwichtenberg, Basic Proof Theory (2nd ed., CUP 2000)", "Negri & von Plato, Structural Proof Theory (CUP 2001)", "Girard, Lafont & Taylor, Proofs and Types (CUP 1989)", "Takeuti, Proof Theory (2nd ed.)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sequent calculus and cut elimination

**Goal:** construct and analyse derivations in Gentzen's sequent calculus, and use the
cut-elimination theorem to get structural facts about proofs — consistency,
disjunction properties, and a backbone for proof search.

## 1. Reading a sequent
Γ ⊢ Δ means: if every formula in Γ holds, then at least one in Δ holds.
- **LK** (classical): Δ may contain any number of formulas.
- **LJ** (intuitionistic): at most one formula on the right. This single restriction is
  what blocks excluded middle (⊢ A ∨ ¬A needs two right formulas mid-derivation).
Axioms: A ⊢ A. Rules come in left/right pairs per connective, plus structural rules
(weakening, contraction, exchange) and **cut**:

  Γ ⊢ Δ, A    A, Γ' ⊢ Δ'
  ───────────────────────  (cut)
       Γ, Γ' ⊢ Δ, Δ'

Cut is "use a lemma A": prove it, then use it.

## 2. Building derivations bottom-up
Start from the goal sequent and apply rules backwards. Every rule except cut has the
**subformula property**: premises contain only subformulas of the conclusion. So
cut-free proof search is a finite, syntax-directed tree for propositional LK — it is a
decision procedure. Practical order:
1. Apply invertible rules first (in LK all propositional rules are invertible in G3-style
   systems; in LJ, →R, ∧R, ∨L, ∧L are, but ∨R and →L are not).
2. For quantifiers: ∀R and ∃L need an **eigenvariable** that is fresh (not free in the
   rest of the sequent). ∀L and ∃R take any term — choosing it is where creativity (and
   unification in automated provers) comes in.
3. Close branches with axioms. A branch that cannot close yields a countermodel.

Use the contraction-free variants (G3c/G3i, Dyckhoff's LJT for intuitionistic
propositional logic) when you want terminating search.

## 3. Cut elimination (Hauptsatz)
Every derivation using cut can be transformed into a cut-free derivation of the same
sequent. Proof idea: induction on (complexity of the cut formula, height of the
derivations above the cut); push cuts upward until they meet axioms, where they vanish.
Consequences you can use directly:
- **Consistency:** the empty sequent ⊢ has no cut-free proof (no rule concludes it), so
  pure logic is consistent.
- **Disjunction property (LJ):** if ⊢ A ∨ B is provable, the last rule of a cut-free
  proof is ∨R, so ⊢ A or ⊢ B. Similarly the existence property for ∃.
- **Interpolation (Craig)** falls out of analysing cut-free proofs.
- **Cost:** eliminating cut can blow proof size up super-exponentially (towers of 2s) —
  lemmas are a genuine compression, not decoration.

## 4. Beyond pure logic: arithmetic and incompleteness
Adding induction axioms for arithmetic reintroduces essential cuts. Gentzen proved the
consistency of Peano Arithmetic by eliminating cuts with a transfinite induction up to
ε₀, which PA itself cannot prove — consistent with Gödel's second incompleteness
theorem: a consistent, effectively axiomatised theory containing enough arithmetic
cannot prove its own consistency. The *proof-theoretic ordinal* (ε₀ for PA) measures
a theory's strength; ordinal analysis computes it for stronger systems.

Gödel's first theorem in user terms: for such a theory T there is a sentence G_T
true in ℕ (if T is sound) but unprovable in T. It is about provability in a fixed
formal system, not about "unknowable truths" in general.

## 5. Relationship to natural deduction
Natural deduction proofs in normal form correspond to cut-free sequent proofs;
normalisation ↔ cut elimination; via Curry–Howard, both correspond to evaluating
λ-terms. Pick sequent calculus for meta-theory and proof search; natural deduction
for writing readable proofs.

## Gotchas
- Dropping contraction or weakening gives substructural logics (linear, relevant,
  affine). Check which structural rules your system includes before using a result.
- Eigenvariable conditions are the most common error in hand derivations.
- Conventions differ (sets vs multisets vs sequences for Γ; explicit vs absorbed
  structural rules). State your variant. Uncertain: exact invertibility lists depend on
  the variant (G1/G3), so verify against your chosen system.

## Verify
- [ ] Calculus variant (LK/LJ, G1/G3, structural rules) stated.
- [ ] Every ∀R/∃L uses a fresh eigenvariable.
- [ ] Each leaf is an axiom; open leaves turned into an explicit countermodel.
- [ ] Any appeal to cut elimination checks it holds for the system used (pure logic vs
      with non-logical axioms).
