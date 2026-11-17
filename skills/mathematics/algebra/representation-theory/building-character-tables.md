---
id: mathematics.algebra.representation-theory.building-character-tables
name: building-character-tables
category: mathematics
field: algebra
product: representation-theory
tags: [representation-theory, character-table, characters, irreducible-representations, irreps, conjugacy-classes, orthogonality-relations, schur-orthogonality, inner-product-of-characters, decomposing-representations, permutation-representation, linear-characters, abelianisation, tensor-product, induced-representation, frobenius-reciprocity, symmetric-group, s3, s4, finite-groups, gap, chemistry-point-groups]
level: advanced
status: draft
description: "Build the complex character table of a small finite group from class sizes, linear characters, permutation characters and orthogonality, then decompose any representation."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building character tables (finite groups, over ℂ)

**Goal:** produce the full table of irreducible characters of a small group G, and use it
to decompose a given representation into irreducibles.

## 1. The constraints you fill the table with
- Rows = irreducible characters, columns = **conjugacy classes**; the table is square
  (number of irreps = number of classes).
- **Σ (dim χᵢ)² = |G|**, and each dim divides |G|.
- **Row orthogonality:** `⟨χ, ψ⟩ = (1/|G|) Σ_classes |C|·χ(g_C)·conj(ψ(g_C)) = δ`.
  Forgetting the class-size weight |C| is the #1 error.
- **Column orthogonality:** `Σᵢ χᵢ(g)·conj(χᵢ(h)) = |C_G(g)|` if g ~ h, else 0. The
  column of the identity gives Σ dim² = |G| again.
- χ(1) = dim; χ(g⁻¹) = conj χ(g); |χ(g)| ≤ χ(1); values are sums of roots of unity.

## 2. Procedure
1. **Classes and sizes.** For Sₙ, classes = cycle types; size = n!/(Π kᵢ^{mᵢ} mᵢ!).
2. **Linear (1-dim) characters** = characters of the abelianisation G/[G,G]; there are
   |G/[G,G]| of them. For Sₙ (n ≥ 2): trivial and sign.
3. **Permutation characters:** if G acts on a set X, `π(g) = #fixed points`. Then
   `π − 1` is a character; it is irreducible iff the action is 2-transitive
   (check ⟨π, π⟩ = 2).
4. **Products:** multiply a known irrep by a linear character (another irrep, possibly
   the same one); take tensor squares and subtract known pieces.
5. **Induce** from a subgroup (Frobenius reciprocity: ⟨Ind χ, ψ⟩_G = ⟨χ, Res ψ⟩_H).
6. **Finish with column orthogonality:** once only one row is missing, solve for it
   from the orthogonality of columns with the identity column.

## 3. Worked example: S₃
Classes: e (1), transpositions (3), 3-cycles (2). Σ dim² = 6 with 3 irreps ⇒ 1, 1, 2.
| | e | (12) | (123) |
|---|---|---|---|
| trivial | 1 | 1 | 1 |
| sign | 1 | −1 | 1 |
| standard | 2 | 0 | −1 |
The standard row is π − 1 for the action on {1,2,3} (fixed points 3, 1, 0).
Check: ⟨std, std⟩ = (4 + 0 + 2·1)/6 = 1 ✓.

S₄ for cross-checking (classes e, (12), (12)(34), (123), (1234) with sizes 1,6,3,8,6):
trivial 1,1,1,1,1; sign 1,−1,1,1,−1; 2-dim 2,0,2,−1,0; standard 3,1,−1,0,−1;
standard⊗sign 3,−1,−1,0,1.

## 4. Decomposing a representation
Given its character ψ (trace on each class — compute only one element per class):
multiplicity of χᵢ in ψ = ⟨ψ, χᵢ⟩. ψ is irreducible ⇔ ⟨ψ, ψ⟩ = 1.
Applications: vibrational modes in chemistry (point groups), symmetry-adapted bases,
counting invariants (multiplicity of trivial = average number of fixed points).

## Gotchas
- Using a class representative's character but forgetting its class size in sums.
- Complex values: conjugate the second argument; non-real values occur (e.g. C₃, A₄)
  and come in conjugate rows.
- Different groups can share a character table (D₄ and Q₈) — the table doesn't
  determine G.
- Real vs complex: over ℝ some irreps merge; this method assumes ℂ.

## Machine check
GAP: `Display(CharacterTable(SymmetricGroup(4)));`, decomposition via
`MatScalarProducts(tbl, Irr(tbl), [psi])` (exact function choice unconfirmed — see GAP
manual, chapter "Class Functions"). See mathematics.algebra.gap.computing-with-groups-in-gap.

## Verify
- [ ] Table is square; dims squared sum to |G|.
- [ ] Every pair of rows is orthogonal with class-size weights; every row has norm 1.
- [ ] Every pair of columns satisfies column orthogonality (identity column too).
- [ ] Decomposition multiplicities are non-negative integers and dimensions add up.
