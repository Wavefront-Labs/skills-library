---
id: mathematics.geometry-and-topology.general-topology.using-compactness-arguments
name: using-compactness-arguments
category: mathematics
field: geometry-and-topology
product: general-topology
tags: [general-topology, point-set-topology, compactness, open-cover, finite-subcover, sequential-compactness, heine-borel, tychonoff, metric-spaces, closed-and-bounded, extreme-value-theorem, uniform-continuity, lebesgue-number-lemma, hausdorff, finite-intersection-property, compact-hausdorff, counterexamples, topological-spaces]
level: advanced
status: draft
description: "Prove and use compactness: open-cover, sequential and Heine–Borel tests, the core consequences, Lebesgue numbers, and the counterexamples that show where each criterion fails."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using compactness arguments

**Goal:** decide whether a space or subset is compact, and use compactness to turn
local or pointwise information into global, uniform conclusions.

## 1. The definitions you can use, and when they agree
- **Compact:** every open cover has a finite subcover.
- **Sequentially compact:** every sequence has a convergent subsequence.
- **Finite intersection property (FIP) form:** every family of closed sets whose finite
  intersections are non-empty has non-empty total intersection.
In **metric spaces** compact ⇔ sequentially compact ⇔ complete and totally bounded.
In general topological spaces neither implies the other — don't swap them silently.

## 2. Proving a set is compact
1. **In ℝⁿ: Heine–Borel** — compact ⇔ closed and bounded. (False in general metric
   spaces: the closed unit ball of ℓ² is closed, bounded, not compact.)
2. **Continuous image** of a compact space is compact.
3. **Closed subset** of a compact space is compact.
4. **Finite unions** and (**Tychonoff**) arbitrary **products** of compact spaces are
   compact.
5. **Quotients** of compact spaces are compact (they are continuous images).
6. Directly: take an arbitrary open cover and extract a finite subcover (e.g. for
   {0} ∪ {1/n}: the set containing 0 swallows all but finitely many points).

## 3. Proving a set is NOT compact
Produce one **explicit** open cover with no finite subcover, or a sequence with no
convergent subsequence (in metric spaces).
- (0, 1): cover by (1/n, 1).
- ℝ: cover by (−n, n).
- Unit ball of ℓ²: basis vectors eₙ satisfy ‖eₙ − eₘ‖ = √2 — no Cauchy subsequence.

## 4. The payoffs (what compactness is for)
- **Extreme value theorem:** continuous f: K → ℝ on compact K attains max and min.
- **Uniform continuity:** continuous on compact metric ⇒ uniformly continuous.
- **Lebesgue number lemma:** every open cover of a compact metric space has δ > 0 such
  that every set of diameter < δ lies in one cover element — the workhorse for
  "small enough pieces lie in one chart" arguments (path lifting, homotopy subdivision).
- **Closed maps:** a continuous map from compact to **Hausdorff** is closed; a
  continuous bijection compact → Hausdorff is a **homeomorphism** (no need to check the
  inverse is continuous).
- **Compact subsets of Hausdorff spaces are closed;** disjoint compact sets in a
  Hausdorff space can be separated by open sets.
- **Local-to-global:** a property holding on a neighbourhood of every point (bounded,
  locally finite, locally Lipschitz bound) holds globally after a finite subcover.

## 5. Argument template (local → global)
"For each x ∈ K choose an open Uₓ ∋ x on which P holds with constant Cₓ. {Uₓ} covers K;
take a finite subcover Uₓ₁,…,Uₓₙ. Then P holds on K with C = max Cₓᵢ."
The finite max (or min of positive numbers) is exactly where compactness is used — point
to it explicitly in the write-up.

## Gotchas
- Compactness is **intrinsic**: a subset is compact iff it is compact in the subspace
  topology; "closed" is relative to the ambient space.
- Non-Hausdorff spaces: compact sets need not be closed; limits need not be unique.
- Taking "the minimum" of infinitely many positive δ's — the infimum can be 0; that is
  the gap compactness fills.
- Tychonoff for infinite products needs the axiom of choice and the **product**
  topology (the box topology fails).

## Verify
- [ ] Stated which definition (cover / sequential / FIP) you used and that it applies
      in this space.
- [ ] Every "finite" step points to a finite subcover.
- [ ] Non-compactness claims come with an explicit cover or sequence.
- [ ] Hausdorff hypothesis checked before using closed-map or homeomorphism results.
