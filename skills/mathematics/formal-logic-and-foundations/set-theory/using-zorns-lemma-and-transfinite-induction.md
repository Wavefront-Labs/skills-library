---
id: mathematics.formal-logic-and-foundations.set-theory.using-zorns-lemma-and-transfinite-induction
name: using-zorns-lemma-and-transfinite-induction
category: mathematics
field: formal-logic-and-foundations
product: set-theory
tags: [set-theory, zfc, axiom-of-choice, zorns-lemma, well-ordering-theorem, transfinite-induction, transfinite-recursion, ordinals, cardinals, chains, partial-order, maximal-element, upper-bound, hamel-basis, maximal-ideal, cardinal-arithmetic, cantor-schroeder-bernstein, countability, limit-ordinal, successor-ordinal]
level: advanced
status: draft
description: "Run a correct Zorn's lemma or transfinite-induction argument: set up the poset, check every chain (including the empty one), handle limit stages, and know when choice is actually needed."
sources: ["Jech, Set Theory (3rd millennium ed., Springer 2003)", "Kunen, Set Theory (College Publications, 2011)", "Halmos, Naive Set Theory (1960)", "Enderton, Elements of Set Theory (1977)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using Zorn's lemma and transfinite induction

**Goal:** prove "a maximal such-and-such exists" or "build an object in ω, ω₁, … many
steps" with a template that doesn't leak — the usual failures are an unchecked chain
case and a mishandled limit stage.

## 1. Zorn's lemma: the template
**Statement.** If (P, ≤) is a non-empty partial order in which every chain has an upper
bound in P, then P has a maximal element. (Equivalent over ZF to the axiom of choice
and the well-ordering theorem.)

Proof skeleton, e.g. "every vector space has a basis":
1. **Define P precisely.** P = the set of linearly independent subsets of V, ordered by ⊆.
   P must be a *set* — define it as a subset of something you already have (here
   𝒫(V)).
2. **Non-empty / empty chain.** ∅ ∈ P. (Many write-ups use the "every chain has an upper
   bound" version, where the empty chain needs an upper bound — i.e. P ≠ ∅. Check it.)
3. **Chains have upper bounds.** For a chain C ⊆ P, take U = ⋃C. Show U ∈ P: a finite
   subset of U lies in a single member of C (because C is totally ordered — **this is
   where the chain property is used**), hence is independent. U bounds C.
4. **Maximal element M exists** by Zorn.
5. **Maximal ⇒ what you want.** If M did not span V, pick v ∉ span(M); M ∪ {v} is
   independent and strictly larger — contradiction.

Step 5 is the real mathematics; step 3 is where proofs are usually wrong. Typical
upper bound: the union for "increasing" structures (ideals, subspaces, partial
functions, filters); the intersection when ordering by ⊇.

Standard applications: maximal ideals in rings with 1 (proper ideals ordered by ⊆;
the union of a chain of proper ideals is proper because it misses 1), Hahn–Banach,
algebraic closures, every filter extends to an ultrafilter, Tychonoff (via ultrafilters
or subbases).

## 2. Transfinite induction and recursion
**Induction:** to prove φ(α) for all ordinals α (or all α < κ), show:
- **zero:** φ(0);
- **successor:** φ(α) ⇒ φ(α + 1);
- **limit:** for limit λ, (∀β < λ φ(β)) ⇒ φ(λ).
The limit case is the one people forget, and the one where the content usually lives.

**Recursion:** define F(α) from F↾α (all earlier values). E.g. building an increasing
chain: F(α+1) extends F(α); F(λ) = ⋃_{β<λ} F(β). You must check the union at limits
still has the property (closed under unions of chains — the same check as Zorn step 3).

**Well-order then recurse** is the constructive face of choice: well-order a set as
{x_α : α < κ}, then decide each x_α in turn using decisions already made. This is how
Hamel bases of ℝ over ℚ, Bernstein sets, and many counterexamples in analysis are
built. Counting arguments at each stage (fewer than continuum many constraints so far)
use |α| < 2^ℵ₀ for α < 𝔠.

## 3. Cardinal arithmetic you will need
- For infinite κ, λ: κ + λ = κ · λ = max(κ, λ). Exponentiation is where independence
  lives (2^ℵ₀ is not determined by ZFC).
- Cantor–Schröder–Bernstein: injections both ways ⇒ bijection; no choice needed.
- A countable union of countable sets is countable — **uses (countable) choice**.
- Comparability of any two cardinals is equivalent to AC.

## 4. When is choice really needed?
Avoid AC if a canonical choice exists (least element of a well-ordered set, a
specific formula). Flag every use: some readers work in ZF + DC (dependent choice), which
suffices for most of analysis (sequential arguments) but not for Hamel bases or
non-measurable sets. Results like "every vector space has a basis" are equivalent to
AC — no AC-free proof exists.

## Gotchas
- Applying Zorn to a proper class (e.g. "all groups") is invalid; bound the size first.
- An upper bound must lie **in P**, not just exist somewhere.
- "Maximal" ≠ "maximum": many maximal elements can exist; Zorn gives existence only.
- Uncertain: terminology for "chain" (totally ordered subset) vs "tower" varies between
  textbooks; state your definition.

## Verify
- [ ] P is a set, its order is stated, and P ≠ ∅ (or the empty chain is handled).
- [ ] The upper bound of an arbitrary chain is shown to lie in P, using totality.
- [ ] The "maximal ⇒ desired property" step is a genuine contradiction argument.
- [ ] Transfinite arguments have explicit zero, successor and **limit** cases.
- [ ] Every use of choice is flagged, with the weakest form needed noted.
