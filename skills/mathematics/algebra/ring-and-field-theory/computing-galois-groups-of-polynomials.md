---
id: mathematics.algebra.ring-and-field-theory.computing-galois-groups-of-polynomials
name: computing-galois-groups-of-polynomials
category: mathematics
field: algebra
product: ring-and-field-theory
tags: [ring-and-field-theory, galois-theory, galois-group, field-extensions, splitting-field, irreducibility, eisenstein-criterion, rational-root-test, discriminant, resolvent-cubic, cubic, quartic, quintic, dedekind-reduction-mod-p, cycle-type, symmetric-group, solvability-by-radicals, abstract-algebra, sage, pari-gp, magma]
level: advanced
status: gated
description: "Determine the Galois group of a rational polynomial: irreducibility tests, discriminant for cubics, resolvent cubic for quartics, reduction mod p, and S_p for prime degree."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Computing Galois groups of polynomials over ℚ

**Goal:** for f ∈ ℚ[x] of small degree, identify Gal(f) as a subgroup of Sₙ (acting on
the roots), and from that read off splitting-field degree and solvability by radicals.

## 1. First: is f irreducible? (Gal is transitive ⇔ yes)
- **Rational root test:** roots p/q with p | constant term, q | leading coefficient.
  Settles degree 2–3 completely.
- **Eisenstein** at a prime p (p divides all lower coefficients, p ∤ leading, p² ∤
  constant). Try a shift x → x + 1 if it fails directly (cyclotomic trick).
- **Reduce mod p** (p ∤ leading coefficient): irreducible mod p ⇒ irreducible over ℚ.
  The converse fails (x⁴ + 1 is reducible mod every prime).
- If reducible, factor and handle factors separately; Gal(f) sits inside the product.

## 2. Degree 3 (irreducible)
Discriminant of `x³ + px + q` is `Δ = −4p³ − 27q²` (depress a general cubic first, or
use the general formula). **Δ a rational square ⇒ A₃ ≅ C₃, otherwise S₃.**
Example: x³ − 2: Δ = −108, not a square ⇒ S₃, splitting field degree 6.

## 3. Degree 4 (irreducible)
For `x⁴ + px² + qx + r` the resolvent cubic (roots α₁α₂ + α₃α₄, etc.) is
`R(y) = y³ − p y² − 4r y + (4pr − q²)`. Conventions differ between texts (some use
roots (α₁+α₂)(α₃+α₄)) — any one works if used consistently; check yours against a
known example. Let Δ = disc(f) (= disc(R)).
| R over ℚ | Δ square? | Gal |
|---|---|---|
| irreducible | no | S₄ |
| irreducible | yes | A₄ |
| splits into 3 linear | — | V₄ |
| exactly one rational root | — | D₄ if f irreducible over ℚ(√Δ), else C₄ |
Example x⁴ − 2: R = y³ + 8y = y(y² + 8), one root ⇒ D₄ or C₄. Δ = −2048, so
ℚ(√Δ) = ℚ(√−2); ℚ(⁴√2, √−2) has degree 8 (⁴√2 is real, √−2 is not), so f stays
irreducible over ℚ(√−2) ⇒ D₄ (order 8).

## 4. Reduction mod p (Dedekind) — fast evidence of cycle types
For a prime p not dividing disc(f) (or the leading coefficient), factor f mod p. If the
irreducible factor degrees are d₁,…,dₖ, then Gal(f) **contains an element of cycle type
(d₁,…,dₖ)**. Collect cycle types over several primes:
- a transposition + an n-cycle + (for prime n, any transposition with transitivity)
  pins Sₙ;
- seeing an odd permutation rules out Aₙ.
It can only prove that elements exist, never that they don't — a group is "confirmed"
small only via resolvents/discriminant.

## 5. Prime degree p shortcut
Irreducible f of prime degree p with **exactly two non-real roots** ⇒ Gal(f) = Sₚ
(complex conjugation is a transposition; transitive subgroup of prime degree contains a
p-cycle). Classic: x⁵ − 4x + 2 (Eisenstein at 2, three real roots by sign changes /
calculus) ⇒ S₅, not solvable by radicals.

## 6. Reading off consequences
- |Gal| = [splitting field : ℚ].
- f solvable by radicals ⇔ Gal solvable (always for degree ≤ 4).
- Intermediate fields ↔ subgroups (Galois correspondence, order-reversing).

## Gotchas
- The discriminant-square test needs f irreducible. Making f monic or substituting
  x → x/c changes Δ only by a square factor, so the verdict survives; a sign slip
  in Δ does not (−3 vs 3 flips the answer).
- Gal depends on the base field: x² + 1 over ℝ is C₂, over ℂ trivial.
- Don't confuse "has a real root" with "reducible over ℚ".

## Machine check
PARI/GP: `polgalois(x^4-2)` (T must be irreducible; degree ≤ 7 built in, 8-11 need the galdata package, per the PARI 2.19 manual).
SymPy (run here): `from sympy.polys.numberfields.galoisgroups import galois_group; galois_group(Poly(x**4-2, x), by_name=True)` returns D4 with discriminant not a square; it also gave S5 for x^5-4x+2, S3 for x^3-2, C3/A3 for x^3-3x+1, V4 for x^4+1 and C4 for x^4-4x^2+2, matching the tables above.
Sage: `NumberField(x^4-2,'a').galois_group().structure_description()` (gated: unconfirmed, source is paywalled or blocked: Sage not installed; check `galois_group?`).

The resolvent cubic y³ − p y² − 4r y + (4pr − q²) agrees with the Dummit-Foote form for roots α₁α₂+α₃α₄; x⁵ − 4x + 2 has three real and two non-real roots (numpy), and the quoted discriminants (−108, −2048) were recomputed.

## Verify
- [ ] Irreducibility established by a named test before using transitivity.
- [ ] |Gal| divides n! and is a multiple of n (transitive).
- [ ] Mod-p cycle types seen are all possible in the claimed group.
- [ ] Computer algebra agrees.
