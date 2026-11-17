---
id: mathematics.algebra.commutative-and-homological-algebra.computing-tor-and-ext
name: computing-tor-and-ext
category: mathematics
field: algebra
product: commutative-and-homological-algebra
tags: [commutative-and-homological-algebra, homological-algebra, commutative-algebra, tor, ext, derived-functors, projective-resolution, free-resolution, injective-resolution, koszul-complex, long-exact-sequence, chain-complex, exact-sequences, tensor-product, hom-functor, modules, abelian-groups, universal-coefficient-theorem, macaulay2, regular-sequence]
level: advanced
status: draft
description: "Compute Tor and Ext of modules by projective resolutions, Koszul complexes and long exact sequences, with worked ℤ-module and polynomial-ring examples and the usual index traps."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Computing Tor and Ext

**Goal:** compute `Torᵢ^R(M, N)` and `Extⁱ_R(M, N)` for concrete modules over a
commutative ring R, and use them (flatness, projective dimension, universal coefficients).

## 1. The recipe
1. Take a **projective (usually free) resolution** of M:
   `… → F₂ → F₁ → F₀ → M → 0`, exact. Drop M.
2. **Tor:** apply `− ⊗_R N` to `F•`, take homology: `Torᵢ(M,N) = Hᵢ(F• ⊗ N)`.
3. **Ext:** apply `Hom_R(−, N)` — the arrows **reverse** — take cohomology:
   `Extⁱ(M,N) = Hⁱ(Hom(F•, N))`.
4. Sanity: `Tor₀ = M ⊗ N`, `Ext⁰ = Hom(M, N)`. Results do not depend on the resolution.
Tor is balanced: resolving N instead gives the same answer — resolve whichever is easier.

## 2. Workhorse examples (over ℤ, write d = gcd(m, n))
Resolution of ℤ/m: `0 → ℤ --·m--> ℤ → ℤ/m → 0`.
- Tensor with ℤ/n: `ℤ/n --·m--> ℤ/n`. Kernel ≅ ℤ/d, cokernel ≅ ℤ/d.
  So `ℤ/m ⊗ ℤ/n ≅ ℤ/d`, `Tor₁(ℤ/m, ℤ/n) ≅ ℤ/d`, higher Tor = 0 (ℤ is a PID).
- Hom into ℤ/n: `ℤ/n --·m--> ℤ/n` again ⇒ `Hom ≅ ℤ/d`, `Ext¹(ℤ/m, ℤ/n) ≅ ℤ/d`.
- Hom into ℤ: `ℤ --·m--> ℤ` ⇒ `Hom(ℤ/m, ℤ) = 0`, `Ext¹(ℤ/m, ℤ) ≅ ℤ/m`.
- Free or flat modules: `Torᵢ(ℚ, −) = 0` for i ≥ 1 (ℚ is flat over ℤ).
These feed the **universal coefficient theorems** in topology.

## 3. Polynomial rings: the Koszul complex
For R = k[x₁,…,xₙ] and M = k = R/(x₁,…,xₙ), the Koszul complex on the regular sequence
x₁,…,xₙ is a free resolution of length n with ranks C(n,i).
n = 2: `0 → R --(−y, x)ᵀ--> R² --(x  y)--> R → k → 0`.
Tensor with k: every map becomes 0 ⇒ `Torᵢ(k, k) ≅ k^{C(n,i)}`, dims 1, 2, 1.
More generally for any regular sequence f₁,…,f_c, the Koszul complex resolves R/(f).

## 4. Long exact sequences (when resolving is painful)
A short exact sequence `0 → N' → N → N'' → 0` gives
`… → Tor₁(M,N'') → M⊗N' → M⊗N → M⊗N'' → 0` and
`0 → Hom(M,N') → Hom(M,N) → Hom(M,N'') → Ext¹(M,N') → …`.
Use known zeros (projective M, injective N, flat modules) to read off the unknown term.

## 5. What they tell you
- M flat ⇔ `Tor₁(M, −) = 0`; projective ⇔ `Ext¹(M, −) = 0`.
- `Ext¹(M, N)` classifies extensions `0 → N → E → M → 0` (Yoneda); 0 means every such
  sequence splits.
- Over a local Noetherian ring, minimal free resolution ranks of k give Betti numbers;
  `pd M < ∞` for all M ⇔ R regular (Auslander–Buchsbaum–Serre).

## Gotchas
- **Ext is contravariant in the first slot:** the complex `Hom(F•, N)` runs
  `Hom(F₀,N) → Hom(F₁,N) → …`; get the direction wrong and you swap kernel and cokernel.
- Forgetting to drop M before applying the functor shifts every index by one.
- `Hom(F, N)` of a matrix map is its **transpose** (with free modules), not the same matrix.
- Over non-PIDs higher Tor/Ext can be nonzero and even infinite in number
  (e.g. R = k[x]/(x²), k has an infinite periodic resolution).
- Non-commutative R: watch left/right module structure; this skill assumes commutative.

## Machine check
Macaulay2: `R = QQ[x,y]; k = coker vars R; Tor_1(k,k)`, `Ext^1(M,N)`, `res M`, `betti res M`.
(Syntax from memory of Macaulay2 1.2x — verify against current docs.)

## Verify
- [ ] Resolution checked exact (composite maps zero, homology zero away from degree 0).
- [ ] Degree-0 results match M ⊗ N and Hom(M, N) computed directly.
- [ ] Tor computed both ways (resolving M, resolving N) agrees, where feasible.
- [ ] Macaulay2/Sage agrees on at least one instance.
