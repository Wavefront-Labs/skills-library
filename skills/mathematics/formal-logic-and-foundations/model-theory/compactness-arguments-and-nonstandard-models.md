---
id: mathematics.formal-logic-and-foundations.model-theory.compactness-arguments-and-nonstandard-models
name: compactness-arguments-and-nonstandard-models
category: mathematics
field: formal-logic-and-foundations
product: model-theory
tags: [model-theory, compactness-theorem, nonstandard-models, nonstandard-analysis, infinitesimals, lowenheim-skolem, elementary-equivalence, elementary-extension, definability, axiomatisability, finite-satisfiability, ultraproducts, los-theorem, first-order-theory, expanding-the-language, new-constants, transfer-principle, quantifier-elimination]
level: advanced
status: draft
description: "Use the compactness theorem as a tool: add constants and axioms to build nonstandard models, prove non-axiomatisability, and transfer finite results, avoiding the usual first-order pitfalls."
sources: ["Marker, Model Theory: An Introduction (Springer GTM 217, 2002)", "Hodges, A Shorter Model Theory (CUP 1997)", "Chang & Keisler, Model Theory (3rd ed.)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compactness arguments and nonstandard models

**Goal:** apply compactness — *a set of first-order sentences has a model iff every
finite subset does* — to manufacture models with exotic elements, and to show that a
property cannot be expressed in first-order logic.

## 1. The standard recipe (add constants, add axioms)
1. **Choose the language L** and a theory T true in the structure you care about
   (often the full theory Th(M) of a standard structure M).
2. **Expand** L with new constant symbols c (or c_i, i ∈ I).
3. **Add axioms** Σ describing the exotic element: e.g. c > n for every numeral n.
4. **Finite satisfiability:** any finite Σ₀ ⊆ T ∪ Σ mentions finitely many new axioms;
   interpret the constants *inside M itself* (c := a large enough standard number).
   Hence Σ₀ has a model.
5. **Compactness ⇒ T ∪ Σ has a model N.** N satisfies T, so it is elementarily
   equivalent to M (if T = Th(M)), yet contains an element above every standard number.

Applications built on exactly this:
- **Nonstandard arithmetic:** models of Th(ℕ) with infinite elements.
- **Nonstandard reals:** from Th(ℝ, all functions/relations), add c with 0 < c < 1/n for
  all n — an infinitesimal. Transfer then lets first-order statements move between ℝ
  and *ℝ (Robinson's nonstandard analysis).
- **Graph colouring (de Bruijn–Erdős):** an infinite graph is k-colourable iff every
  finite subgraph is. Constants for vertices, propositional letters for "v has colour
  i", finite pieces satisfiable by hypothesis.

## 2. Proving something is *not* first-order axiomatisable
Pattern: suppose a theory T captures exactly the class K. Add axioms forcing an object
"outside K", show finite satisfiability using structures in K, conclude a model of T
not in K — contradiction.
- **Finiteness:** if T had arbitrarily large finite models, then T has an infinite
  model (add sentences "there are ≥ n elements"). So "finite" is not axiomatisable;
  neither is "torsion group" or "connected graph" (add two constants with no path of
  length ≤ n between them, for every n).
- **Well-ordering, ℕ up to isomorphism, Archimedean fields:** none are first-order
  characterisable for the same reason.

## 3. Löwenheim–Skolem complements compactness
A countable theory with an infinite model has models of every infinite cardinality
(upward via compactness with many constants plus distinctness axioms; downward via
Skolem hulls). So no first-order theory with an infinite model pins down that model up
to isomorphism. Second-order "categorical" axiomatisations (Peano with full induction,
complete ordered field) escape this only by leaving first-order logic — and losing
compactness and completeness.

## 4. Ultraproducts: compactness made concrete
Given structures M_i and a non-principal ultrafilter U on I, the ultraproduct ∏M_i/U
satisfies a sentence iff U-almost all M_i do (Łoś's theorem). This gives explicit
nonstandard models (∏ℝ/U on ℕ is a hyperreal field) and an alternative proof of
compactness. Non-principal ultrafilters need (a weak form of) choice.

## 5. Transferring results
If a first-order sentence holds in all fields of characteristic 0, then (compactness)
it holds in all fields of characteristic p for sufficiently large p — the
Lefschetz-style principle used e.g. in the Ax–Grothendieck theorem argument. Check the
statement is genuinely first-order in the chosen language before transferring.

## Gotchas
- **Expressibility is everything.** "For all subsets", "for all n ∈ ℕ" quantifying over
  standard naturals inside a model, "finitely many" — not first-order; compactness says
  nothing about them.
- Constants must be *new*; reusing a symbol of L breaks step 4.
- Finite satisfiability must be checked for **every** finite subset, typically by noting
  each mentions only finitely many of the new axioms.
- Uncertain: some textbooks state compactness for countable languages only in early
  chapters; the general version needs choice (via ultrafilters or Henkin + Zorn).

## Verify
- [ ] Language, base theory and the new constants/axioms are written out explicitly.
- [ ] Finite satisfiability shown by interpreting new constants in a known structure.
- [ ] Every property used is expressed by first-order sentences of the stated language.
- [ ] The conclusion is about elementary equivalence/models of T, not isomorphism.
