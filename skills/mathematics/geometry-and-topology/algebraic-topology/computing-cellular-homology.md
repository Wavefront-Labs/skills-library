---
id: mathematics.geometry-and-topology.algebraic-topology.computing-cellular-homology
name: computing-cellular-homology
category: mathematics
field: geometry-and-topology
product: algebraic-topology
tags: [algebraic-topology, homology, cellular-homology, cw-complex, cell-complex, boundary-map, chain-complex, smith-normal-form, betti-numbers, torsion, euler-characteristic, torus, klein-bottle, projective-plane, rp2, mayer-vietoris, simplicial-homology, sage, topological-data-analysis, tda]
level: advanced
status: gated
description: "Compute homology groups of CW complexes from cell structures and attaching words: cellular boundary maps, Smith normal form for torsion, Euler-characteristic checks, worked surfaces."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Computing cellular homology

**Goal:** compute Hₙ(X; ℤ) for a space with a CW (cell) structure — surfaces, projective
spaces, quotients of polygons — quickly and with torsion right.

## 1. Pipeline
1. **Choose a CW structure** with as few cells as possible. Polygon-with-identifications
   surfaces: one 2-cell, the edge classes as 1-cells, the vertex classes as 0-cells.
2. **Cellular chain groups** `Cₙ = ℤ^{#n-cells}`.
3. **Boundary maps** dₙ: Cₙ → Cₙ₋₁ as integer matrices:
   - d₁(edge from v to w) = w − v (0 for a loop).
   - d₂(2-cell attached along a word in the edges) = for each edge, the **sum of its
     exponents** in the word. `aba⁻¹b⁻¹` gives 0·a + 0·b; `abab⁻¹` gives 2a + 0b.
   - Higher: degree of the attaching map onto each (n−1)-cell (for RPⁿ: 1 + (−1)ⁿ).
4. **Check** dₙ₋₁ ∘ dₙ = 0.
5. **Homology** `Hₙ = ker dₙ / im dₙ₊₁`. Compute with **Smith normal form** of dₙ₊₁:
   diagonal entries 1 contribute nothing, entries k > 1 contribute ℤ/k torsion, and
   free rank = dim ker dₙ − rank dₙ₊₁.

## 2. Worked surfaces (one 0-cell unless noted)
| space | word | d₂ | H₀ | H₁ | H₂ |
|---|---|---|---|---|---|
| torus T² | aba⁻¹b⁻¹ | 0 | ℤ | ℤ² | ℤ |
| Klein bottle | abab⁻¹ | (2, 0) | ℤ | ℤ ⊕ ℤ/2 | 0 |
| RP² | aa | (2) | ℤ | ℤ/2 | 0 |
| genus-g orientable | Π[aᵢ,bᵢ] | 0 | ℤ | ℤ^{2g} | ℤ |
| sphere S² | (one 0-cell, one 2-cell) | — | ℤ | 0 | ℤ |
Non-orientable closed surface ⇔ H₂ = 0 and torsion ℤ/2 in H₁.
RPⁿ: one cell in each dimension, dₖ = 1 + (−1)ᵏ (so 0 for k odd, 2 for k even);
H_k = ℤ/2 for odd k < n, 0 for even 0 < k ≤ n, and Hₙ = ℤ if n is odd.

## 3. Checks that catch most errors
- **Euler characteristic:** Σ(−1)ⁿ(#n-cells) = Σ(−1)ⁿ rank Hₙ. Torus: 1 − 2 + 1 = 0.
- H₀ = ℤ^{#path components}.
- For a closed connected n-manifold: Hₙ = ℤ if orientable, 0 otherwise.
- H₁ is the abelianisation of π₁ (Hurewicz) — compare if you know π₁.

## 4. When you lack a small CW structure
- **Mayer–Vietoris:** X = A ∪ B with open A, B:
  `… → Hₙ(A∩B) → Hₙ(A) ⊕ Hₙ(B) → Hₙ(X) → Hₙ₋₁(A∩B) → …`. Identify the maps,
  not just the groups — exactness alone rarely pins Hₙ(X).
- **Long exact sequence of a pair** and excision; `H̃ₙ(X/A) ≅ Hₙ(X, A)` for good pairs.
- **Künneth** for products; **universal coefficients** for other coefficients
  (ℤ/2 coefficients ignore orientation issues: Klein bottle has H₂(K; ℤ/2) = ℤ/2).

## 5. Machine check
Sage (simplicial complexes): `simplicial_complexes.Torus().homology()` → `{0: 0, 1: Z x Z, 2: Z}` (reduced H₀) (gated: unconfirmed, source is paywalled or blocked: Sage not installed, output not run).
For a hand-built chain complex use `ChainComplex({1: d1, 2: d2}, degree=-1).homology()` (`degree` is an alias of `degree_of_differential` in the Sage reference).
SymPy alternative (run here): `smith_normal_form(Matrix(d2), domain=ZZ)` from `sympy.matrices.normalforms`; with it the table above (torus, Klein bottle, RP²) and RPⁿ for n ≤ 6 were reproduced.
TDA libraries (GUDHI, Ripser) compute homology of point-cloud complexes, usually over a
field — they will not show torsion.

## Gotchas
- Exponent sums, not counts: `a a⁻¹` contributes 0, `a a` contributes 2.
- Using vertex identifications wrongly: count vertex classes after **all**
  identifications, or d₁ is wrong.
- Field coefficients (ℚ, ℤ/2) kill or change torsion — say which coefficients.
- Reduced vs unreduced H₀ (Sage reports reduced by default).

## Verify
- [ ] d∘d = 0 for every pair of consecutive maps.
- [ ] Euler characteristic from cells equals that from Betti numbers.
- [ ] Results match a known example of the same type (table above).
- [ ] Torsion read from Smith normal form, not from rank alone.
