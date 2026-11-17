---
id: mathematics.algebra.group-theory.classifying-small-groups-with-sylow
name: classifying-small-groups-with-sylow
category: mathematics
field: algebra
product: group-theory
tags: [group-theory, abstract-algebra, sylow-theorems, sylow-subgroups, p-groups, finite-groups, group-order, normal-subgroup, simple-groups, semidirect-product, cyclic-groups, abelian-groups, element-counting, lagrange-theorem, cauchy-theorem, classification-of-groups, order-pq, group-actions, class-equation, gap]
level: advanced
status: verified
description: "Use the Sylow theorems, element counting and semidirect products to show a group of given order is not simple or to list all groups of that order."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Classifying small finite groups with Sylow — the standard playbook

**Goal:** given |G| = n, prove G has a normal subgroup (so is not simple), or determine
every group of order n up to isomorphism.

## 1. The tools, stated in usable form
Write `n = pᵃ·m` with p ∤ m.
- **Sylow I:** a subgroup of order pᵃ exists.
- **Sylow II:** all Sylow p-subgroups are conjugate.
- **Sylow III:** `n_p ≡ 1 (mod p)` and `n_p | m`.
- **Consequence:** `n_p = 1` ⇔ the Sylow p-subgroup is **normal**.
- **Lagrange:** element and subgroup orders divide n. **Cauchy:** for every prime p | n
  there is an element of order p.
- Groups of order p or p² are abelian (Zₚ; Z_{p²} or Zₚ×Zₚ). p-groups have nontrivial
  centre (class equation).

## 2. Playbook: "show no group of order n is simple"
1. Factor n. For each prime list allowed n_p (divisors of m that are ≡ 1 mod p).
2. If some n_p is forced to 1 — done.
3. Otherwise **count elements**: distinct Sylow p-subgroups of prime order p intersect
   trivially, so they contribute `n_p(p − 1)` elements of order p. If the minimum counts
   over all primes exceed n, contradiction.
   Example n = 30: n₃ ∈ {1, 10}, n₅ ∈ {1, 6}. If n₃ = 10 and n₅ = 6: 20 + 24 = 44 > 30.
   So one is normal.
4. If counting fails, use the **action on Sylow subgroups** (or cosets): G acts on the
   n_p Sylow subgroups, giving `G → S_{n_p}`. If G is simple the kernel is trivial,
   so n | n_p! (indeed |G| divides n_p!/2 when the image lies in A_{n_p}). Example
   n = 48: n₂ ∈ {1, 3}; n₂ = 3 forces 48 | 3! = 6, impossible, so the kernel is a
   nontrivial proper normal subgroup.

## 3. Playbook: "list all groups of order n"
1. Find a normal Sylow subgroup N and a complement H (another Sylow for the other prime).
   If N ⊴ G, N ∩ H = 1, |N||H| = n, then **G ≅ N ⋊_φ H** for some `φ: H → Aut(N)`.
2. Enumerate homomorphisms φ up to the equivalences that give isomorphic groups
   (conjugate images in Aut(N), automorphisms of H). Trivial φ gives the direct product.
3. **Order pq, p < q:** Sylow q is normal. If p ∤ q − 1, G ≅ Z_{pq} (e.g. 15, 33, 35).
   If p | q − 1 there is exactly one non-abelian group as well (e.g. order 6: S₃;
   order 21: Z₇ ⋊ Z₃).
4. Known counts to check against: order 8 → 5 groups (Z₈, Z₄×Z₂, Z₂³, D₄, Q₈);
   order 12 → 5; order 16 → 14. If your list disagrees, look again.

## Gotchas
- Sylow subgroups of order p² can intersect nontrivially — the element-counting trick
  as stated needs prime order (or careful handling of intersections).
- n_p must divide **m**, not n; using n gives spurious options.
- Two different φ can give isomorphic semidirect products; two "different-looking"
  presentations may be the same group. Distinguish by invariants: centre, number of
  elements of each order, abelianisation.
- Q₈ is not a semidirect product of proper subgroups — the semidirect playbook does not
  find every group of prime-power order.

## Machine check
GAP (see mathematics.algebra.gap.computing-with-groups-in-gap):
`NumberSmallGroups(12);` → 5, and `List(AllSmallGroups(12), StructureDescription);`
names them. `IsSimpleGroup(G)` (not `IsSimple`), `SylowSubgroup(G, p)` confirm individual claims.
The group counts 5, 5, 14 for orders 8, 12, 16 match OEIS A000001; the `NumberSmallGroups`/`AllSmallGroups`/`StructureDescription` names and the "orders up to 2000 except 1024" range are in the GAP SmallGrp manual (GAP itself was not run here). The allowed n_p lists for n = 30 and 48 were recomputed by script.

## Verify
- [ ] Listed n_p from the divisors of m only, with the ≡ 1 (mod p) filter.
- [ ] Every claimed isomorphism type is distinguished by an invariant from the others.
- [ ] Count of groups matches `NumberSmallGroups(n)` in GAP for n < 2000 (excluding 1024).
- [ ] Any "simple" conclusion is consistent with the known list (smallest non-abelian
      simple group has order 60).
